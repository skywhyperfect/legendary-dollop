const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

// Инициализируем клиента с сохранением сессии локально
// При перезапуске не нужно будет заново сканировать QR
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
        // Использовать системный хром, если стандартный не работает на Mac M1/M2
        // executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    }
});

const FASTAPI_WEBHOOK_URL = 'http://localhost:8000/api/bot/whatsapp-webhook';
const FASTAPI_AUTH_URL = 'http://localhost:8000/api/bot/whatsapp-auth';

async function updateAuthStatus(status, qr_data = null) {
    try {
        await axios.post(FASTAPI_AUTH_URL, { status, qr_data });
    } catch (e) {
        // Игнорируем ошибку при недоступности
    }
}

console.log('Инициализация WhatsApp Web Client...');
updateAuthStatus('pending');

client.on('qr', (qr) => {
    console.log('\n======================================================');
    console.log('ОТСКАНИРУЙТЕ ЭТОТ QR-КОД В ВАШЕМ ПРИЛОЖЕНИИ WHATSAPP');
    console.log('======================================================\n');
    qrcode.generate(qr, { small: true });
    
    // Передаем новый QR на бэкенд, чтобы он показал его на фронте
    updateAuthStatus('qr', qr);
});

client.on('authenticated', () => {
    console.log('🔓 Авторизация пройдена (authenticated)!');
    updateAuthStatus('ready');
});

client.on('ready', () => {
    console.log('✅ WhatsApp Client успешно подключен и готов к работе!');
    console.log('Слушаю входящие сообщения...');
    updateAuthStatus('ready');
});

client.on('message', async msg => {
    // Получаем контакт отправителя
    const contact = await msg.getContact();
    const senderName = contact.name || contact.pushname || msg.from;
    
    console.log(`\n📥 Новое сообщение от: ${senderName}`);
    console.log(`ID Чата (chatId) : ${msg.from}`);
    console.log(`Текст: ${msg.body}`);

    // ОГРАНИЧЕНИЕ ДЛЯ ХАКАТОНА: Слушаем только нашу группу
    const allowedGroup = "120363407134966766@g.us";
    if (msg.from !== allowedGroup && !msg.from.includes(allowedGroup)) {
        console.log(`⏭ Игнорирую сообщение (не из целевой группы)`);
        return;
    }

    // Отправляем на наш FastAPI Backend webhook
    try {
        const response = await axios.post(FASTAPI_WEBHOOK_URL, {
            sender: senderName,
            text: msg.body,
            source: 'whatsapp',
            chatId: msg.from
        });
        
        console.log(`📡 Отправлено в Покойо. Статус: ${response.data.status}`);
        
        // Опционально: отправить галочку (реакцию) в самом WhatsApp
        // await msg.react('🤖');
        
    } catch (error) {
        console.error('❌ Ошибка отправки на бэкенд. Убедитесь, что FastAPI запущен на порту 8000.');
        if (error.response) {
            console.error(`Детали: ${error.response.status} ${error.response.data}`);
        }
    }
});

// ─── Добавляем HTTP сервер для приема команд на рассылку из FastAPI ───
const http = require('http');

const server = http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/send') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', async () => {
            try {
                const payload = JSON.parse(body);
                const chatId = payload.chatId; // ID группы или номера
                const text = payload.text;
                
                if (chatId && text) {
                    await client.sendMessage(chatId, text);
                    console.log(`[BROADCAST] Успешно отправлено в ${chatId}`);
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ status: 'success' }));
                } else {
                    res.writeHead(400);
                    res.end(JSON.stringify({ error: 'Missing chatId or text' }));
                }
            } catch (err) {
                console.error('[BROADCAST ERROR]', err);
                res.writeHead(500);
                res.end(JSON.stringify({ error: err.toString() }));
            }
        });
    } else {
        res.writeHead(404);
        res.end();
    }
});

server.listen(3000, () => {
    console.log('📡 WhatsApp-Bridge готов принимать рассылки на порту 3000 (/send)');
});

client.initialize();
