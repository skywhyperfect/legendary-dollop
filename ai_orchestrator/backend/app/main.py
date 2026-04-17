from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import parser, rag, schedule, voice, auth, tasks
from app.ai.rag_service import init_rag
from app.db.database import engine, Base

# Авторегистрация таблиц БД
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этап запуска приложения (startup)
    print("Инициализация RAG Vectorstore...")
    init_rag()
    yield
    # Этап остановки приложения (shutdown)
    print("Завершение работы...")

app = FastAPI(title="AI Завуч Оркестратор API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parser.router, prefix="/api", tags=["parser"])
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["schedule"])
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Backend is running!"}
