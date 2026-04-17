from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import TaskReminder
from typing import List

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    assignee: str
    deadline: str

class TaskResponse(TaskCreate):
    id: int
    is_completed: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskReminder).all()

@router.post("/")
def create_task(req: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskReminder(title=req.title, assignee=req.assignee, deadline=req.deadline)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskReminder).filter(TaskReminder.id == task_id).first()
    if task:
        task.is_completed = True
        db.commit()
        return {"status": "ok"}
    return {"status": "error", "detail": "Task not found"}
