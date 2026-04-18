from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class TaskReminder(Base):
    __tablename__ = "task_reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    assignee = Column(String)
    deadline = Column(String)
    is_accepted = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
