from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.voice_to_task import process_voice_command

router = APIRouter()

class VoicePayload(BaseModel):
    audio_base64: Optional[str] = None
    test_text: Optional[str] = None # Для отладочных кейсов MVP

@router.post("/task")
async def handle_voice_task(payload: VoicePayload):
    # Принимает либо base64 аудио, либо просто текст (чтобы сразу тестировать логику LLM парсера)
    result = process_voice_command(test_text=payload.test_text)
    
    # Можно симулировать ссылки на карточки:
    links = [f"https://dashboard.example.com/task/{i}" for i in range(len(result.tasks))]
    
    return {
        "voice_decomposition": result,
        "task_links": links
    }
