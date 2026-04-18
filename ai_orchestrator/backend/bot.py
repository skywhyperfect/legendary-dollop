"""
Покойо Telegram Bot
======================
Запуск: python bot.py (параллельно с uvicorn backend)

Команды:
  /start          — Приветствие, инструкция
  /svod           — Сводка посещаемости за сегодня (для директора)
  /incidents      — Список активных инцидентов
  /zamena <имя>   — Найти замену учителю

Учителя просто пишут обычные сообщения:
  "1А - 25 детей, двое болеют"
  "В кабинете 302 сломался проектор"
  "Аскар заболел, не придёт"
"""

import os
import sys
import json
import sqlite3
import logging
import re
import requests
from datetime import datetime
from typing import Optional

# ─── Токен из .env ────────────────────────────────────────────
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8618652793:AAGLUa7jV7WjZmEdmtfOq-kuKDJIudjbs5U")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
# Ищем базу там, где запущен бот (рядом с main.py)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orchestrator.db")
if not os.path.exists(DB_PATH):
    # fallback: database rядом с bot.py
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "orchestrator.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger("bot")

# ─── Telegram API helpers ─────────────────────────────────────

BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def tg_get(method: str, params: dict = None):
    r = requests.get(f"{BASE}/{method}", params=params, timeout=10)
    return r.json()

def tg_post(method: str, data: dict):
    r = requests.post(f"{BASE}/{method}", json=data, timeout=10)
    return r.json()

def send(chat_id: int, text: str, parse_mode: str = "HTML"):
    tg_post("sendMessage", {"chat_id": chat_id, "text": text, "parse_mode": parse_mode})

# ─── SQLite для сводок ────────────────────────────────────────

def _get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
    except:
        pass
    return conn

def init_bot_db():
    """Создаём таблицы для бота в том же SQLite."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tg_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            sender TEXT,
            text TEXT,
            parsed_type TEXT,
            parsed_summary TEXT,
            food_class TEXT,
            food_count INTEGER,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()

def save_message(chat_id: int, sender: str, text: str,
                 parsed_type: str, summary: str,
                 food_class: Optional[str] = None,
                 food_count: Optional[int] = None):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO tg_messages (chat_id, sender, text, parsed_type, parsed_summary, food_class, food_count) "
        "VALUES (?,?,?,?,?,?,?)",
        (chat_id, sender, text, parsed_type, summary, food_class, food_count)
    )
    conn.commit()
    conn.close()

def get_food_svod() -> dict:
    """Суммируем все food-сообщения сегодня."""
    conn = _get_conn()
    today = datetime.now().strftime("%Y-%m-%d")
    rows = conn.execute(
        "SELECT food_class, food_count FROM tg_messages "
        "WHERE parsed_type='food' AND date(created_at)=?",
        (today,)
    ).fetchall()
    conn.close()
    total = sum(r[1] for r in rows if r[1])
    classes = {r[0]: r[1] for r in rows if r[0]}
    return {"total": total, "count": len(rows), "classes": classes}

def get_incidents() -> list:
    """Инциденты за сегодня."""
    conn = sqlite3.connect(DB_PATH)
    today = datetime.now().strftime("%Y-%m-%d")
    rows = conn.execute(
        "SELECT sender, parsed_summary, created_at FROM tg_messages "
        "WHERE parsed_type='incident' AND date(created_at)=? ORDER BY created_at DESC LIMIT 10",
        (today,)
    ).fetchall()
    conn.close()
    return [{"sender": r[0], "summary": r[1], "time": r[2]} for r in rows]

# ─── Парсер сообщений (regex + backend LLM) ──────────────────

def extract_food_info(text: str):
    """
    Извлекает класс и количество из текста.
    Поддерживает fuzzy-форматы:
      "1А - 25 детей", "2Б: 22 ребёнка, 3 болеют", "3В — 20",
      "23 из 25", "все пришли кроме Алмаса", "1А: 24 (+2 опоздали)"
    """
    # Ищем класс: 1А, 2Б, 3В, 4Г и т.д.
    class_match = re.search(r"(\d+[АаБбВвГг])", text, re.IGNORECASE)
    food_class = class_match.group(1).upper() if class_match else None
    
    # Паттерн 1: "25 детей", "22 ребёнка", "20 человек"
    count_match = re.search(r"(\d+)\s*(детей|ребёнка|ребенка|человек|уч[её]ников|порций)", text, re.IGNORECASE)
    
    # Паттерн 2: "23 из 25" → берём первое число (присутствующих)
    if not count_match:
        ratio_match = re.search(r"(\d+)\s*из\s*(\d+)", text)
        if ratio_match:
            return food_class, int(ratio_match.group(1))
    
    # Паттерн 3: "все пришли" / "все на месте" (без числа)
    if not count_match:
        if re.search(r"все\s*(пришли|на месте|здесь|есть)", text, re.IGNORECASE):
            return food_class, None  # Тип food, но без числа
    
    # Паттерн 4: "24 (+2 опоздали)" → 24
    if not count_match:
        paren_match = re.search(r"(\d+)\s*\(", text)
        if paren_match:
            return food_class, int(paren_match.group(1))
    
    food_count = int(count_match.group(1)) if count_match else None
    return food_class, food_count

def local_classify(text: str) -> dict:
    """
    Быстрая классификация без LLM (работает без API ключа).
    Поддерживает fuzzy NLP для грязного ввода.
    Returns dict с type, urgency, summary.
    """
    t = text.lower()
    food_class, food_count = extract_food_info(text)

    # Расширенное определение food-сообщений (fuzzy)
    food_keywords = ["детей", "ребёнок", "порций", "кухня", "столовая", "пришли", "на месте", "из 25", "из 24", "из 23", "из 22", "из 20"]
    if food_class or food_count or any(w in t for w in food_keywords):
        # Извлекаем количество отсутствующих: "кроме Алмаса и Диаса" = 2
        absent_names = re.findall(r"кроме\s+([А-ЯЁа-яё]+(?:\s+и\s+[А-ЯЁа-яё]+)*)", text, re.IGNORECASE)
        absent_count = 0
        if absent_names:
            absent_count = absent_names[0].count(" и ") + 1
        
        sick_match = re.search(r"(\d+)\s*(болеют|отсутствуют|нет)", text, re.IGNORECASE)
        sick_count = int(sick_match.group(1)) if sick_match else absent_count
        
        summary = f"Явка: {food_count or '?'} чел." + (f" ({food_class})" if food_class else "")
        if sick_count > 0:
            summary += f", отсутствует: {sick_count}"
        return {"type": "food", "urgency": "low", "summary": summary,
                "food_class": food_class, "food_count": food_count}

    if any(w in t for w in ["заболел", "болеет", "не придёт", "не придет", "нетрудоспособ", "температур", "больничн"]):
        teacher = re.search(r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+|[А-ЯЁ][а-яё]+", text)
        name = teacher.group(0) if teacher else "Учитель"
        return {"type": "absence", "urgency": "high",
                "summary": f"Отсутствует: {name}. Требуется замена.",
                "food_class": None, "food_count": None}

    if any(w in t for w in ["сломал", "поломка", "не работает", "протечка", "авария", "драка", "конфликт", "разбил", "упал"]):
        return {"type": "incident", "urgency": "high",
                "summary": f"Инцидент: {text[:80]}",
                "food_class": None, "food_count": None}

    return {"type": "other", "urgency": "low",
            "summary": text[:100],
            "food_class": None, "food_count": None}

def parse_message_backend(text: str) -> dict:
    """Отправляем на бэкенд. Если недоступен — используем local_classify."""
    try:
        r = requests.post(
            f"{BACKEND_URL}/api/parse-message",
            json={"text": text, "user_id": 0},
            timeout=5
        )
        if r.status_code == 200:
            data = r.json()
            food_class, food_count = extract_food_info(text)
            data["food_class"] = food_class
            data["food_count"] = food_count
            return data
    except Exception as e:
        log.warning(f"Backend unavailable, using local parser: {e}")
    return local_classify(text)

# ─── Обработка команд/сообщений ──────────────────────────────

def handle_start(chat_id: int, first_name: str):
    send(chat_id, f"""👋 <b>Привет, {first_name}!</b>

Я — <b>Покойо</b>, ваш AI-Оркестратор школы Aqbobek 🏫

<b>Учителям — просто напишите:</b>
• <i>«1А — 25 детей, 2 болеют»</i>
• <i>«В каб. 302 сломался проектор»</i>
• <i>«Аскар заболел, не придёт»</i>

<b>Директору (команды):</b>
/svod — 📊 Сводка посещаемости
/incidents — 🚨 Активные инциденты
/zamena [имя] — 🔄 Найти замену
/demo — 🎬 Заполнить тестовыми данными
/help — ❓ Помощь

Всё остальное я разберу сам.""")

def handle_help(chat_id: int):
    send(chat_id, """❓ <b>Помощь по командам</b>

<b>Учителям</b> — просто напишите обычное сообщение:
  <code>1А - 25 детей, 2 болеют</code>
  <code>В кабинете 12 сломалась парта</code>
  <code>Аскар Болатов заболел</code>

<b>Директору:</b>
  /svod — сводка порций по всем классам за сегодня
  /incidents — список инцидентов
  /zamena Аскар — найти замену учителю
  /demo — заполнить базу тестовыми данными для демо

📊 Дашборд: <a href='http://localhost:5173'>localhost:5173</a>""")

def handle_demo(chat_id: int):
    """Засеиваем базу демо-данными для красивого питча."""
    demo_messages = [
        ("Абенова Г.",  "1А — 24 детей, 1 болеет",   "food",    "Явка: 24 чел. (1А)",    "1А", 24),
        ("Сейткали М.", "1Б: 22 ребёнка",              "food",    "Явка: 22 чел. (1Б)",    "1Б", 22),
        ("Нурланова Д.","2А — 26 детей, все пришли",   "food",    "Явка: 26 чел. (2А)",    "2А", 26),
        ("Касымова А.", "2Б — 23 человека",            "food",    "Явка: 23 чел. (2Б)",    "2Б", 23),
        ("Жаксыбеков", "3В — 20 детей, 2 болеют",     "food",    "Явка: 20 чел. (3В)",    "3В", 20),
        ("Смирнова Е.", "4А — 25 человек",             "food",    "Явка: 25 чел. (4А)",    "4А", 25),
        ("Аскар Б.",   "Аскар заболел, не приду",    "absence", "Отсутствует: Аскар. Требуется замена.", None, None),
        ("Ахмет З.",   "В кабинете 302 сломался проектор", "incident", "Инцидент: сломан проектор в каб.302", None, None),
    ]
    conn = sqlite3.connect(DB_PATH)
    # Очищаем сегодняшние записи, чтобы не дублировались
    today = datetime.now().strftime("%Y-%m-%d")
    conn.execute("DELETE FROM tg_messages WHERE date(created_at)=?", (today,))
    for sender, text, mtype, summary, cls, cnt in demo_messages:
        conn.execute(
            "INSERT INTO tg_messages (chat_id, sender, text, parsed_type, parsed_summary, food_class, food_count) VALUES (?,?,?,?,?,?,?)",
            (chat_id, sender, text, mtype, summary, cls, cnt)
        )
    conn.commit()
    conn.close()
    send(chat_id, """🎬 <b>Демо-данные загружены!</b>

Добавлено:
• 📋 6 отчётов об явке (1А–4А)
• 🚨 1 инцидент (проектор 302)
• 🔴 1 случай отсутствия (Аскар)

Теперь введите /svod или /incidents — и покажите жюри! 🎯""")

def handle_svod(chat_id: int):
    data = get_food_svod()
    if data["count"] == 0:
        send(chat_id, "📊 <b>Сводка за сегодня</b>\n\nСообщений от учителей пока нет.")
        return

    lines = [f"📊 <b>Сводка по питанию — {datetime.now().strftime('%d.%m.%Y')}</b>\n"]
    for cls, cnt in sorted(data["classes"].items()):
        lines.append(f"  {cls}: <b>{cnt}</b> порций")
    lines.append(f"\n🍽 <b>ИТОГО: {data['total']} порций</b>")
    lines.append(f"📝 Получено отчётов: {data['count']}")
    lines.append(f"\n✅ Автоматически сформировано Покойо")
    send(chat_id, "\n".join(lines))

def handle_incidents(chat_id: int):
    incidents = get_incidents()
    if not incidents:
        send(chat_id, "🚨 <b>Инциденты за сегодня</b>\n\nИнцидентов не зафиксировано ✅")
        return

    lines = [f"🚨 <b>Инциденты за {datetime.now().strftime('%d.%m.%Y')}</b>\n"]
    for i, inc in enumerate(incidents, 1):
        time_str = inc["time"][-8:-3] if len(inc["time"]) > 8 else inc["time"]
        lines.append(f"{i}. [{time_str}] <b>{inc['sender']}</b>: {inc['summary']}")
    send(chat_id, "\n".join(lines))

def handle_zamena(chat_id: int, teacher_name: str):
    if not teacher_name.strip():
        send(chat_id, "❓ Укажите имя: <code>/zamena Аскар</code>")
        return
    send(chat_id, f"🔄 Ищу замену для <b>{teacher_name}</b>...")
    try:
        r = requests.post(
            f"{BACKEND_URL}/api/schedule/substitute",
            json={"teacher_name": teacher_name},
            timeout=8
        )
        if r.status_code == 200:
            plan = r.json().get("substitution_plan", [])
            if not plan:
                send(chat_id, f"⚠️ Свободных учителей для замены <b>{teacher_name}</b> не найдено.")
                return
            lines = [f"✅ <b>План замен для {teacher_name}:</b>\n"]
            for sub in plan:
                lines.append(f"• Урок {sub.get('lesson_number')} | {sub.get('class_name')} | "
                              f"<b>{sub.get('substitute_teacher')}</b>")
            send(chat_id, "\n".join(lines))
        else:
            send(chat_id, "⚠️ Ошибка при поиске замены.")
    except Exception:
        send(chat_id, "⚠️ Бэкенд недоступен. Запустите сервер.")

def handle_text(chat_id: int, sender: str, text: str):
    """Основная логика: парсим сообщение учителя."""
    parsed = parse_message_backend(text)

    msg_type = parsed.get("type", "other")
    summary = parsed.get("summary", text[:80])
    food_class = parsed.get("food_class")
    food_count = parsed.get("food_count")

    save_message(chat_id, sender, text, msg_type, summary, food_class, food_count)

    # Ответ учителю
    if msg_type == "food":
        porции_str = f"{food_count} порций" if food_count else "данные"
        class_str = f" ({food_class})" if food_class else ""
        send(chat_id, f"✅ Принято{class_str}: <b>{porции_str}</b>\nДанные добавлены в сводку директора.")

    elif msg_type == "absence":
        send(chat_id, f"🚨 <b>Зафиксировано отсутствие.</b>\n{summary}\n\nДиректор уведомлён. AI ищет замену...")

    elif msg_type == "incident":
        send(chat_id, f"⚠️ <b>Инцидент зафиксирован.</b>\n{summary}\nКарточка создана на дашборде директора.")

    else:
        send(chat_id, f"📝 Принято. Сообщение добавлено в журнал.")

# ─── Polling loop ─────────────────────────────────────────────

def run_polling():
    log.info("🤖 Покойо Telegram Bot запущен (polling mode)")
    log.info(f"Backend: {BACKEND_URL}")

    init_bot_db()

    # Проверяем, что токен рабочий
    me = tg_get("getMe")
    if not me.get("ok"):
        log.error(f"❌ Неверный токен: {me}")
        sys.exit(1)
    bot_name = me["result"]["username"]
    log.info(f"✅ Бот авторизован: @{bot_name}")

    offset = 0
    while True:
        try:
            updates = tg_get("getUpdates", {"offset": offset, "timeout": 30})
            if not updates.get("ok"):
                continue

            for upd in updates.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg:
                    continue

                chat_id = msg["chat"]["id"]
                text = msg.get("text", "").strip()
                user = msg.get("from", {})
                sender = user.get("first_name", "") + " " + user.get("last_name", "")
                sender = sender.strip() or user.get("username", "Аноним")

                if not text:
                    continue

                log.info(f"[{chat_id}] {sender}: {text[:60]}")

                # Команды
                if text.startswith("/start"):
                    handle_start(chat_id, user.get("first_name", "Пользователь"))
                elif text.startswith("/help"):
                    handle_help(chat_id)
                elif text.startswith("/demo"):
                    handle_demo(chat_id)
                elif text.startswith("/svod"):
                    handle_svod(chat_id)
                elif text.startswith("/incidents"):
                    handle_incidents(chat_id)
                elif text.startswith("/zamena"):
                    parts = text.split(maxsplit=1)
                    teacher = parts[1] if len(parts) > 1 else ""
                    handle_zamena(chat_id, teacher)
                else:
                    handle_text(chat_id, sender, text)

        except KeyboardInterrupt:
            log.info("Бот остановлен.")
            break
        except requests.exceptions.ReadTimeout:
            # Нормальное явление для long-polling, просто продолжаем
            pass
        except requests.exceptions.ConnectionError:
            log.warning("Нет соединения с Telegram. Повтор через 5 сек...")
            import time; time.sleep(5)
        except Exception as e:
            log.error(f"Ошибка: {e}")
            import time; time.sleep(2)

if __name__ == "__main__":
    run_polling()
