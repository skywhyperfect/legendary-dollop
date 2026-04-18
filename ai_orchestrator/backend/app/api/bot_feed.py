"""
API роутер для Telegram-бот данных.
Позволяет дашборду получать реальные сообщения учителей из SQLite.
"""
import sqlite3
import os
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Ищем orchestrator.db: сначала рядом с main.py (в backend/), потом в backend/app/
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(_backend_dir, "orchestrator.db")
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(_backend_dir, "..", "orchestrator.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_table():
    try:
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
    except Exception:
        pass


import re
from pydantic import BaseModel

class WhatsAppWebhookReq(BaseModel):
    sender: str
    text: str
    source: str
    chatId: str

def _extract_food_info(text):
    class_match = re.search(r"(\d+[АаБбВвГг])", text, re.IGNORECASE)
    count_match = re.search(r"(\d+)\s*(детей|ребёнка|ребенка|человек|учеников|порций)", text, re.IGNORECASE)
    food_class = class_match.group(1).upper() if class_match else None
    food_count = int(count_match.group(1)) if count_match else None
    return food_class, food_count

def _local_classify(text):
    t = text.lower()
    food_class, food_count = _extract_food_info(text)
    if food_class or food_count or any(w in t for w in ["детей", "ребёнок", "порций", "столовая"]):
        return "food", f"Явка: {food_count or '?'} чел." + (f" ({food_class})" if food_class else ""), food_class, food_count
    if any(w in t for w in ["заболел", "болеет", "не придёт", "не придет", "нетрудоспособ"]):
        return "absence", f"Отсутствие, требуется замена: {text[:60]}", None, None
    if any(w in t for w in ["сломал", "поломка", "не работает", "протечка", "авария", "драка", "конфликт"]):
        return "incident", f"Инцидент: {text[:80]}", None, None
    return "other", text[:100], None, None

# Global state for WA authentication
wa_auth_state = {
    "status": "pending",  # pending, qr, ready, error
    "qr_data": None
}

class WhatsAppAuthReq(BaseModel):
    status: str
    qr_data: str = None

@router.post("/whatsapp-auth")
def update_whatsapp_auth(req: WhatsAppAuthReq):
    """Обновляет состояние авторизации WhatsApp из Node.js клиента."""
    wa_auth_state["status"] = req.status
    wa_auth_state["qr_data"] = req.qr_data
    return {"ok": True}

@router.get("/whatsapp-auth-status")
def get_whatsapp_auth_status():
    """Фронтенд опрашивает этот эндпоинт для показа QR-кода."""
    return wa_auth_state

@router.post("/whatsapp-webhook")
def whatsapp_webhook(req: WhatsAppWebhookReq):
    """Принимает сообщения от реального WhatsApp и вставляет в ту же базу."""
    _ensure_table()
    mtype, summary, food_class, food_count = _local_classify(req.text)
    try:
        conn = _get_conn()
        conn.execute(
            """INSERT INTO tg_messages 
               (chat_id, sender, text, parsed_type, parsed_summary, food_class, food_count) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (req.chatId, req.sender, f"[WA] {req.text}", mtype, summary, food_class, food_count)
        )
        conn.commit()
        conn.close()
        return {"status": "ok", "parsed_type": mtype}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/messages")
def get_bot_messages(limit: int = 50):
    """Последние сообщения от учителей из Telegram-бота или WhatsApp."""
    _ensure_table()
    try:
        conn = _get_conn()
        rows = conn.execute(
            "SELECT id, sender, text, parsed_type, parsed_summary, food_class, food_count, created_at "
            "FROM tg_messages ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in reversed(rows)]
    except Exception as e:
        return []

@router.delete("/clear")
def clear_feed():
    try:
        conn = _get_conn()
        conn.execute("DELETE FROM tg_messages")
        conn.commit()
        conn.close()
        return {"status": "ok", "message": "Feed cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/svod")
def get_food_svod():
    """Сводка по питанию за сегодня."""
    _ensure_table()
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        conn = _get_conn()
        rows = conn.execute(
            "SELECT food_class, food_count FROM tg_messages "
            "WHERE parsed_type='food' AND date(created_at)=?",
            (today,)
        ).fetchall()
        incidents = conn.execute(
            "SELECT COUNT(*) as cnt FROM tg_messages "
            "WHERE parsed_type='incident' AND date(created_at)=?",
            (today,)
        ).fetchone()
        absences = conn.execute(
            "SELECT COUNT(*) as cnt FROM tg_messages "
            "WHERE parsed_type='absence' AND date(created_at)=?",
            (today,)
        ).fetchone()
        conn.close()

        total = sum(r["food_count"] for r in rows if r["food_count"])
        classes = {r["food_class"]: r["food_count"] for r in rows if r["food_class"]}
        return {
            "total_portions": total,
            "report_count": len(rows),
            "classes": classes,
            "incidents_today": incidents["cnt"] if incidents else 0,
            "absences_today": absences["cnt"] if absences else 0,
            "date": today,
        }
    except Exception as e:
        return {"total_portions": 0, "report_count": 0, "classes": {}, "incidents_today": 0, "absences_today": 0}
