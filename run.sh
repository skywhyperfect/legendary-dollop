#!/bin/bash

echo "=========================================="
echo "🚀 Запуск Покойо — AI-Оркестратор Школы (AIS Hack 3.0)"
echo "=========================================="

# Check for fallback mode
FALLBACK_MODE=false
if [ "$1" == "--fallback" ]; then
    FALLBACK_MODE=true
    echo "⚠️  ВКЛЮЧЕН FALLBACK-РЕЖИМ (без WhatsApp/Node.js)"
fi

cd ai_orchestrator

# Проверка наличия .env
if [ ! -f ".env" ]; then
    echo "❌ Ошибка: Файл .env не найден в ai_orchestrator!"
    echo "Пожалуйста, скопируйте .env.example в .env и настройте переменные."
    exit 1
fi

# Функция для корректного завершения всех процессов при нажатии Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Остановка всех сервисов AI-Завуч..."
    # Убиваем все фоновые задачи (jobs)
    kill $(jobs -p) 2>/dev/null
    exit
}

# Перехватываем сигналы остановки (Ctrl+C)
trap cleanup SIGINT SIGTERM EXIT

echo "🧹 Очистка старых (зависших) процессов на портах..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
sleep 1

echo "📦 1. Запуск Backend (FastAPI)..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
# Используем python3 -m uvicorn для надежности
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
cd ..

echo "⏳ Ожидание 3 секунды для запуска Backend..."
sleep 3

echo "🤖 2. Запуск Telegram-бота..."
cd backend
python3 bot.py &
cd ..

if [ "$FALLBACK_MODE" = false ]; then
    echo "⏳ Ожидание 2 секунды..."
    sleep 2
    echo "📱 3. Запуск WhatsApp Bridge (Node.js)..."
    cd whatsapp
    npm start &
    cd ..
else
    echo "⏭️  Пропуск WhatsApp Bridge (Fallback-режим)"
fi

echo "⏳ Ожидание 2 секунды..."
sleep 2

echo "💻 4. Запуск Frontend (React Vite)..."
cd frontend
npm run dev -- --host 0.0.0.0 &
cd ..

echo "=========================================="
echo "✅ Все сервисы запущены в фоне!"
if [ "$FALLBACK_MODE" = false ]; then
    echo "⚠️  Ожидайте появление QR-кода для WhatsApp чуть ниже."
fi
echo "➡️  В браузере введите: http://localhost:5173"
echo "Нажмите [Ctrl+C] для одновременной остановки всех сервисов."
echo "=========================================="

# Ждем завершения всех фоновых процессов (бесконечно, пока не нажмут Ctrl+C)
wait
