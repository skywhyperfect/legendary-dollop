#!/bin/bash

echo "=========================================="
echo "🚀 Запуск AI-Завуч (AIS Hack 3.0)"
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

echo "📦 1. Запуск Backend (FastAPI)..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
uvicorn app.main:app --reload --port 8000 &
cd ..

echo "📱 2. Запуск WhatsApp Bridge (Node.js)..."
cd whatsapp
npm start &
cd ..

echo "💻 3. Запуск Frontend (React Vite)..."
cd frontend
npm run dev &
cd ..

echo "=========================================="
echo "✅ Все сервисы запущены в фоне!"
echo "➡️  Frontend: http://localhost:5173"
echo "➡️  Backend: http://localhost:8000"
echo "⚠️  Внимательно смотрите логи выше: скоро здесь появится QR-код для WhatsApp."
echo "Нажмите [Ctrl+C] для одновременной остановки всех сервисов."
echo "=========================================="

# Ждем завершения всех фоновых процессов (бесконечно, пока не нажмут Ctrl+C)
wait
