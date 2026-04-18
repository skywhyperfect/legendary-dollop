const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const express = require('express');
const app = express();
app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const RETRY_DELAY_MS = 5000;
let initInProgress = false;
let retryTimer = null;

client.on('qr', (qr) => {
    console.log('Пожалуйста, отсканируйте этот QR-код в приложении WhatsApp (Связанные устройства):');
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('WhatsApp Client готов! Слушаю входящие сообщения...');
    initInProgress = false;
});

client.on('disconnected', (reason) => {
    console.warn(`[WA] Клиент отключился: ${reason}`);
    scheduleReinit();
});

client.on('auth_failure', (msg) => {
    console.error(`[WA] Ошибка авторизации: ${msg}`);
    scheduleReinit();
});

client.on('message', async msg => {
    // Ждем сообщения (включая сообщения из групп)
    console.log(`[WA] Входящее сообщение от ${msg.from}: ${msg.body}`);
    
    // Передаем сообщение на наш единый FastAPI парсер
    try {
        const payload = {
            text: msg.body,
            user_id: 0, // Условный ID для MVP
            platform: 'whatsapp'
        };
        
        console.log("Отправка в Парсер...");
        const response = await axios.post(`${BACKEND_URL}/api/parse-message`, payload);
        const data = response.data;
        
        let type_emoji = "ℹ️";
        if (data.type === 'absence') type_emoji = "🤒";
        if (data.type === 'incident') type_emoji = "🚨";
        if (data.type === 'food') type_emoji = "🍱";
        
        // Формируем красивый ответ по результатам парсинга
        let reply = `${type_emoji} *Получено AI Завучем*\n`;
        reply += `Тип: ${data.type}\n`;
        reply += `Суть: ${data.summary}\n`;
        
        if (data.substitution_plan && data.substitution_plan.length > 0) {
            reply += `\n*План замен:*\n`;
            data.substitution_plan.forEach(sub => {
                reply += `- Замена на ${sub.lesson_number} уроке: ${sub.substitute_teacher}\n`;
            });
        }
        
        await msg.reply(reply);
        
    } catch (error) {
        console.error("Ошибка при связи с FastAPI:", error.message);
    }
});

function isRecoverableInitError(err) {
    const text = String(err && (err.stack || err.message || err)).toLowerCase();
    return (
        text.includes('execution context was destroyed') ||
        text.includes('protocol error') ||
        text.includes('target closed') ||
        text.includes('navigation')
    );
}

function scheduleReinit() {
    if (retryTimer) return;
    retryTimer = setTimeout(() => {
        retryTimer = null;
        startClient();
    }, RETRY_DELAY_MS);
}

async function startClient() {
    if (initInProgress) return;
    initInProgress = true;

    try {
        console.log('[WA] Инициализация клиента...');
        await client.initialize();
    } catch (err) {
        initInProgress = false;
        if (isRecoverableInitError(err)) {
            console.warn(`[WA] Временная ошибка инициализации, повтор через ${RETRY_DELAY_MS / 1000}с: ${err.message}`);
            scheduleReinit();
            return;
        }
        console.error('[WA] Критическая ошибка инициализации:', err);
        scheduleReinit();
    }
}

process.on('unhandledRejection', (reason) => {
    console.error('[WA] unhandledRejection:', reason);
    if (isRecoverableInitError(reason)) {
        scheduleReinit();
    }
});

process.on('uncaughtException', (err) => {
    console.error('[WA] uncaughtException:', err);
    if (isRecoverableInitError(err)) {
        scheduleReinit();
        return;
    }
    process.exit(1);
});

startClient();

// Эндпоинт для отправки сообщений из Backend
app.post('/send', async (req, res) => {
    const { chatId, text } = req.body;
    console.log(`[WA] Получен запрос на отправку в ${chatId}: ${text}`);
    try {
        if (!client || !client.info) {
            console.warn('[WA] Попытка отправки до инициализации клиента');
            return res.status(503).json({ error: 'WhatsApp client is not ready' });
        }
        await client.sendMessage(chatId, text);
        console.log(`[WA] Сообщение успешно отправлено в ${chatId}`);
        res.json({ status: 'success' });
    } catch (error) {
        console.error('[WA] Ошибка при отправке сообщения:', error.message);
        res.status(500).json({ error: error.message });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`🚀 WA Bridge Server готов и слушает на порту ${PORT}`);
});
