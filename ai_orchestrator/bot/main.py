import asyncio
import os
import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "mock_token")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Здравствуйте! Я AI-ассистент (Оркестратор). Готов принимать ваши сообщения и голосовые.")

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("Анализирую сообщение...")
    
    # Отправляем сообщение на backend
    try:
        async with aiohttp.ClientSession() as session:
            payload = {"text": message.text, "user_id": message.from_user.id}
            async with session.post(f"{BACKEND_URL}/api/parse-message", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    type_emoji = {
                        "absence": "🤒",
                        "incident": "🚨",
                        "food": "🍱",
                        "other": "ℹ️"
                    }.get(data.get("type", "other"), "ℹ️")
                    
                    reply = (
                        f"{type_emoji} **Успешно обработано**\n"
                        f"Тип: {data.get('type')}\n"
                        f"Срочность: {data.get('urgency')}\n"
                        f"Суть: {data.get('summary')}\n"
                    )
                    await message.answer(reply, parse_mode="Markdown")
                else:
                    await message.answer("Проблема со связью с бэкендом AI.")
    except Exception as e:
        logging.error(f"Error calling backend: {e}")
        await message.answer("Ошибка: Сервер интеллекта недоступен.")

async def main():
    if TELEGRAM_BOT_TOKEN == "mock_token":
        logging.warning("Используется заглушка для токена. Вставьте реальный токен в .env")
        return
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
