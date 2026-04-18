#!/bin/bash

echo "=========================================="
echo "🚀 Запуск Покойо — AI-Оркестратор Школы (AIS Hack 3.0)"
echo "=========================================="

cd ai_orchestrator

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

echo "📦 1. Запуск Backend (FastAPI) и Telegram-бота..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
# Используем python3 -m uvicorn для надежности
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
python3 bot.py &
cd ..

echo "📱 2. Запуск WhatsApp Bridge (Node.js)..."
cd whatsapp
npm start &
cd ..

echo "💻 3. Запуск Frontend (React Vite)..."
cd frontend
npm run dev -- --host 0.0.0.0 &
cd ..

echo "=========================================="
echo "✅ Все сервисы запущены в фоне!"
echo "📡 Теперь вы можете открывать систему с ДРУГИХ устройств (телефона, планшета)!"
echo "➡️  В браузере телефона введите: http://<IP-вашего-мака>:5173"
echo "=========================================="
echo "⚠️  Внимательно смотрите логи выше: скоро здесь появится QR-код для WhatsApp."
echo "Нажмите [Ctrl+C] для одновременной остановки всех сервисов."
echo "=========================================="

# Ждем завершения всех фоновых процессов (бесконечно, пока не нажмут Ctrl+C)
wait
