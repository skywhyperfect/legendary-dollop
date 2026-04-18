import os
import json
import openai
from pydantic import BaseModel, Field
from typing import List, Optional
from app.data_loader import load_staff
from app.ai.rag_service import check_compliance
from app.ai.llm_parser import parse_with_llm, ParsedMessage

class TaskItem(BaseModel):
    assignee: str = Field(description="Роль или Имя исполнителя")
    deadline: str = Field(description="Дедлайн задачи, если указан")
    description: str = Field(description="Описание задачи")
    rag_compliance: Optional[str] = Field(default=None, description="Результат проверки приказами (RAG)")

class TaskDecomposition(BaseModel):
    general_context: str = Field(description="Общий контекст записи (например 'Мы делаем хакатон')")
    tasks: List[TaskItem] = Field(description="Список выделенных задач")
    substitution_triggered: Optional[list] = Field(default=None, description="План замен, если триггернулась болезнь (Smart Substitution)")

def transcribe_audio(file_path: str) -> str:
    """ Whisper transcription (Mock/Real) """
    # В реальном коде: audio_file= open(file_path, "rb"); return openai.Audio.transcribe("whisper-1", audio_file).text
    return "Завхозу починить трубу в кулере до обеда"

def process_voice_command(test_text: str = None, file_path: str = None) -> TaskDecomposition:
    api_key = os.getenv("OPENAI_API_KEY", "mock")
    
    text = test_text if test_text else transcribe_audio(file_path)
    
    # 1. Сначала пропускаем через основной парсер, вдруг это болезнь (Smart Substitution)
    general_parse = parse_with_llm(text)
    substitution = general_parse.dict().get("substitution_plan") if general_parse.type == "absence" else None
    
    # 2. Вытаскиваем задачи через отдельный Function Call
    if api_key in ["mock", "test_mock"]:
        # Mock ответ для тестирования без ключа
        tasks = []
        if "Айгерим" in text or "актовый зал" in text.lower():
            tasks.append(TaskItem(assignee="Айгерим", deadline="Среда", description="Подготовить актовый зал (освещение, сцена)", rag_compliance="Соответствует нормам пожарной безопасности"))
        if "Назкен" in text or "воду" in text.lower():
            tasks.append(TaskItem(assignee="Назкен", deadline="Завтра", description="Заказать воду для всех классов", rag_compliance="Без нарушений"))
        if "Ахмет" in text or "трубы" in text.lower() or "парту" in text.lower():
            tasks.append(TaskItem(assignee="Ахмет (Завхоз)", deadline="Сегодня", description="Проверить трубы на 2 этаже / Починить парту", rag_compliance="Проверка пройдена"))
        if "Аскар" in text or "заболел" in text.lower():
            tasks.append(TaskItem(assignee="Завуч", deadline="Срочно", description="Найти замену Аскару (Математика)", rag_compliance="Норма №110 учтена"))
            
        return TaskDecomposition(
            general_context=text,
            tasks=tasks,
            substitution_triggered=substitution
        )
        
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты голосовой интеллект-ассистент Покойо. Разбей транскрипцию голоса директора на четкие задачи."},
                {"role": "user", "content": text}
            ],
            functions=[
                {
                    "name": "break_into_tasks",
                    "description": "Разбивка текста на дискретные задачи",
                    "parameters": TaskDecomposition.model_json_schema()
                }
            ],
            function_call={"name": "break_into_tasks"}
        )
        data = json.loads(response.choices[0].message.function_call.arguments)
        
        # 3. Для каждой задачи прогоняем легкий RAG-чек (если, например, упоминают деньги или питание/приказы)
        if "tasks" in data:
            for task in data["tasks"]:
                compliance = check_compliance(task.get("description", ""))
                task["rag_compliance"] = compliance.get("analysis", "Без нарушений")
                
        data["substitution_triggered"] = substitution
        return TaskDecomposition(**data)
    except Exception as e:
        print(f"Error parsing task: {e}")
        return TaskDecomposition(general_context=text, tasks=[], substitution_triggered=substitution)
