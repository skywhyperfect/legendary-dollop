#!/bin/bash

echo "🚀 Запуск AI Оркестратор..."

# Backend
echo "Запускаю FastAPI Backend..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..
sleep 4

# Telegram Bot
echo "Запускаю Telegram Bot..."
cd bot
python main.py &
TG_PID=$!
cd ..
sleep 2

# WhatsApp Listener
echo "Запускаю WhatsApp Слушатель..."
cd whatsapp_bot
npm start &
WA_PID=$!
cd ..
sleep 2

# React Frontend
echo "Запускаю React Frontend..."
cd frontend
npm run dev &
FRONT_PID=$!
cd ..

echo ""
echo "✅ Все сервисы запущены!"
echo "Backend:  http://<ваш-ip-или-localhost>:8000"
echo "Frontend: http://<ваш-ip-или-localhost>:5173"
echo "WhatsApp: QR-код будет в консоли"
echo ""
echo "Для остановки нажмите Ctrl+C"

wait
