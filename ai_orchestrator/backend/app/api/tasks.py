from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import TaskReminder
from typing import List
import re
import urllib.request
import json

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    assignee: str
    deadline: str

class TaskResponse(TaskCreate):
    id: int
    is_accepted: bool
    is_completed: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    all_tasks = db.query(TaskReminder).all()
    
    def get_keywords(text):
        # Очищаем и берем только КОРНИ слов (первые 4-5 букв), чтобы игнорировать окончания (воду/воды)
        words = re.sub(r'[^а-яА-Яa-zA-Z\s]', '', text.lower()).split()
        return {w[:4] for w in words if len(w) > 3}

    def is_similar(t1, t2):
        # 1. Проверка имен (агрессивный prefix match)
        n1 = re.sub(r'[^а-яА-Яa-zA-Z]', '', t1.assignee.lower())
        n2 = re.sub(r'[^а-яА-Яa-zA-Z]', '', t2.assignee.lower())
        names_match = (n1[:4] == n2[:4] or n1 in n2 or n2 in n1)
        
        # 2. Проверка сути по корням слов
        k1 = get_keywords(t1.title)
        k2 = get_keywords(t2.title)
        if not k1 or not k2: return False
        
        intersection = k1.intersection(k2)
        # Если есть хоть 2 общих смысловых корня или более 40% совпадения
        overlap = len(intersection) / min(len(k1), len(k2))
        return names_match and (overlap >= 0.4 or len(intersection) >= 2)

    # Умная дедупликация
    final_tasks = []
    # Сортируем от новых к старым (ID DESC)
    sorted_all = sorted(all_tasks, key=lambda x: x.id, reverse=True)
    
    for t in sorted_all:
        is_dup = False
        for existing in final_tasks:
            if is_similar(t, existing):
                is_dup = True
                break
        if not is_dup:
            final_tasks.append(t)
            
    return final_tasks

@router.post("/")
def create_task(req: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskReminder(title=req.title, assignee=req.assignee, deadline=req.deadline)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # ─── Рассылка в WhatsApp. Voice-to-Task напрямую ───
    try:
        # Без выдуманного шаблона, используем реальные вытащенные ИИ данные
        payload = {
            "chatId": "120363407134966766@g.us",
            "text": f"🎙 *Делегирована новая задача*\n👤 Кому: {req.assignee}\n📌 Задача: {req.title}\n⏱ Срок: {req.deadline}"
        }
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request("http://localhost:3000/send", data=data, method='POST')
        request.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(request, timeout=2) as response:
            pass
    except Exception as e:
        print(f"WhatsApp Broadcast failed: {e}")
        
    return new_task

@router.put("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskReminder).filter(TaskReminder.id == task_id).first()
    if task:
        task.is_completed = True
        db.commit()
        return {"status": "ok"}
    return {"status": "error", "detail": "Task not found"}
