from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.llm_parser import parse_with_llm, ParsedMessage

router = APIRouter()

class MessagePayload(BaseModel):
    text: str
    user_id: int

@router.post("/parse-message", response_model=ParsedMessage)
async def parse_message(payload: MessagePayload):
    # В реальном приложении здесь было бы сохранение в БД
    # Но для MVP мы просто возвращаем разобранный JSON
    parsed_data = parse_with_llm(payload.text)
    
    # TODO: В будущем здесь будет логика обновления базы инцидентов / замен
    return parsed_data
