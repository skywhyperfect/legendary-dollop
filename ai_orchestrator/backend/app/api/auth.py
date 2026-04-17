from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import User
import hashlib

router = APIRouter()

class AuthRequest(BaseModel):
    email: str
    password: str

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register(req: AuthRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == req.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    
    new_user = User(email=req.email, password_hash=get_password_hash(req.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Успешная регистрация", "user_id": new_user.id}

@router.post("/login")
def login(req: AuthRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == req.email).first()
    if not db_user or db_user.password_hash != get_password_hash(req.password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    
    return {"message": "Успешный вход", "token": f"fake-jwt-token-{db_user.id}"}
