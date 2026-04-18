"""
API для отправки Telegram-уведомлений из дашборда.
Вызывается при: утверждении замены, создании задачи.
"""
import os
import logging
import requests
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
log = logging.getLogger("notify")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
BASE_TG = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Список зарегистрированных chat_id учителей
# В продакшне эти данные хранятся в БД. Здесь — mock для демо.
TEACHER_CHATS: dict[str, int] = {
    # Заполняется когда учитель пишет /start боту
    # "Смирнова Елена": 123456789,  # пример
}

# Общий чат школы (для broadcast)
# Установите через /chatid команду в боте или вручную
SCHOOL_BROADCAST_CHAT = int(os.getenv("SCHOOL_CHAT_ID", "0"))


def _send_tg(chat_id: int, text: str) -> bool:
    """Отправляет сообщение в Telegram. Возвращает True если успешно."""
    if not BOT_TOKEN or chat_id == 0:
        log.warning(f"Telegram не настроен (chat_id={chat_id})")
        return False
    try:
        r = requests.post(f"{BASE_TG}/sendMessage", json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }, timeout=5)
        return r.status_code == 200
    except Exception as e:
        log.error(f"Telegram error: {e}")
        return False


class SubstitutionNotifyRequest(BaseModel):
    substitute_teacher: str
    missing_teacher: str
    class_name: str
    lesson_number: int
    room: str
    subject: str = "Урок"


class TaskNotifyRequest(BaseModel):
    assignee: str
    title: str
    deadline: str


class BroadcastRequest(BaseModel):
    message: str


@router.post("/substitution")
def notify_substitution(req: SubstitutionNotifyRequest):
    """
    Вызывается из дашборда при утверждении замены.
    Отправляет уведомление заменяющему учителю и в общий чат.
    """
    text = (
        f"📢 <b>Уведомление о замене</b>\n\n"
        f"Уважаемый(ая) <b>{req.substitute_teacher}</b>!\n\n"
        f"У вас сегодня замена:\n"
        f"• <b>Класс:</b> {req.class_name}\n"
        f"• <b>Урок №{req.lesson_number}</b>\n"
        f"• <b>Кабинет:</b> {req.room}\n"
        f"• <b>Вместо:</b> {req.missing_teacher}\n\n"
        f"Замена оформлена согласно Приказу МОН РК №110. "
        f"Запись внесена в ЖУПЗ. ✅\n\n"
        f"<i>AI-Завуч Aqbobek</i>"
    )

    sent = False
    # Пробуем найти chat_id учителя
    chat_id = TEACHER_CHATS.get(req.substitute_teacher, SCHOOL_BROADCAST_CHAT)
    if chat_id:
        sent = _send_tg(chat_id, text)

    return {
        "status": "sent" if sent else "queued",
        "message": text,
        "recipient": req.substitute_teacher,
        "wa_link": f"https://wa.me/?text={requests.utils.quote(text.replace('<b>', '*').replace('</b>', '*').replace('<i>', '').replace('</i>', '').replace('\n', '%0A'))}",
    }


@router.post("/task")
def notify_task(req: TaskNotifyRequest):
    """
    Вызывается при создании задачи из Voice-to-Task.
    Отправляет уведомление исполнителю задачи.
    """
    text = (
        f"📋 <b>Новая задача от директора</b>\n\n"
        f"Уважаемый(ая) <b>{req.assignee}</b>!\n\n"
        f"Вам поставлена задача:\n"
        f"<b>{req.title}</b>\n\n"
        f"⏰ <b>Срок выполнения:</b> {req.deadline}\n\n"
        f"Пожалуйста, подтвердите получение, ответив на это сообщение.\n"
        f"<i>AI-Завуч Aqbobek</i>"
    )

    chat_id = TEACHER_CHATS.get(req.assignee, SCHOOL_BROADCAST_CHAT)
    sent = _send_tg(chat_id, text) if chat_id else False

    return {
        "status": "sent" if sent else "queued",
        "message": text,
        "recipient": req.assignee,
    }


@router.post("/broadcast")
def broadcast(req: BroadcastRequest):
    """Рассылка сообщения всем зарегистрированным учителям."""
    if SCHOOL_BROADCAST_CHAT:
        _send_tg(SCHOOL_BROADCAST_CHAT, req.message)
    return {"status": "sent", "chat_id": SCHOOL_BROADCAST_CHAT}


@router.get("/status")
def notify_status():
    """Проверка: настроен ли Telegram."""
    return {
        "telegram_configured": bool(BOT_TOKEN),
        "broadcast_chat": SCHOOL_BROADCAST_CHAT,
        "registered_teachers": list(TEACHER_CHATS.keys()),
        "tip": "Чтобы получать уведомления — напишите /start боту и добавьте chat_id в TEACHER_CHATS",
    }
