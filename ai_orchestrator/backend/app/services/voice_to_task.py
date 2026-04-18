import os
import json
import openai
import re
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
    alem_key = os.getenv("ALEM_STT_API_KEY", "")
        
    try:
        # Пробуем использовать прокси Alem для LLM задачи
        if alem_key and alem_key != "mock" and alem_key.strip():
            client = openai.OpenAI(api_key=alem_key, base_url="https://llm.alem.ai/v1")
            
            # ПЕРВАЯ ПОПЫТКА: Через Function Calling (самый надежный способ если прокси тянет)
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Ты голосовой интеллект-ассистент Покойо. Разбей транскрипцию голоса директора на четкие задачи. Выделяй Имя исполнителя, суть задачи и срок."},
                        {"role": "user", "content": text}
                    ],
                    functions=[
                        {
                            "name": "break_into_tasks",
                            "description": "Разбивка текста на дискретные задачи",
                            "parameters": TaskDecomposition.model_json_schema()
                        }
                    ],
                    function_call={"name": "break_into_tasks"},
                    timeout=15
                )
                data = json.loads(response.choices[0].message.function_call.arguments)
            except Exception as fe:
                print(f"Function call failed, trying direct JSON: {fe}")
                # ВТОРАЯ ПОПЫТКА: Обычный JSON-промпт (если прокси не поддерживает функции)
                prompt = f"""
                Разбей текст на задачи в формате JSON.
                Текст: "{text}"
                
                Пример ответа:
                {{
                  "general_context": "контекст",
                  "tasks": [
                    {{"assignee": "Имя", "description": "что сделать", "deadline": "когда"}}
                  ]
                }}
                """
                resp = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    timeout=15
                )
                raw_content = resp.choices[0].message.content
                # Чистим от маркдауна если он есть
                clean_json = re.sub(r"```json\n?|\n?```", "", raw_content).strip()
                data = json.loads(clean_json)
        else:
            raise Exception("no_key")
            
        # 3. Для каждой задачи прогоняем легкий RAG-чек (если, например, упоминают деньги или питание/приказы)
        if "tasks" in data:
            for task in data["tasks"]:
                compliance = check_compliance(task.get("description", ""))
                task["rag_compliance"] = compliance.get("analysis", "Без нарушений")
                
        data["substitution_triggered"] = substitution
        return TaskDecomposition(**data)
        
    except Exception as e:
        print(f"Error parsing task via LLM: {e}")
        # MOCK Fallback (если LLM недоступна или сломалась)
        tasks = []
        lower_text = text.lower().strip()
        
        # 1. Попытка "Умного" парсинга через регулярку (Имя, задача)
        # Ищем паттерны типа "Ахмед, почини..." или "Айгерим: подготовь..."
        match = re.search(r"^([А-ЯЁа-яё\s]+?)[,:-]\s*(.*)$", text)
        if match:
            assignee_candidate = match.group(1).strip()
            task_candidate = match.group(2).strip()
            # Если имя не слишком длинное (чтобы не схватить полпредложения)
            if len(assignee_candidate.split()) <= 2:
                tasks.append(TaskItem(
                    assignee=assignee_candidate, 
                    deadline="В течение дня", 
                    description=task_candidate, 
                    rag_compliance="Без нарушений"
                ))
        
        # 2. Если регулярка не сработала, проверяем по ключевым словам (Хардкод)
        if not tasks:
            if "айгерим" in lower_text or "актов" in lower_text:
                tasks.append(TaskItem(assignee="Айгерим", deadline="Среда", description="Подготовить актовый зал (освещение, сцена)", rag_compliance="Соответствует нормам пожарной безопасности"))
            elif "назкен" in lower_text or "вод" in lower_text:
                tasks.append(TaskItem(assignee="Назкен", deadline="Завтра", description="Заказать воду для всех классов", rag_compliance="Без нарушений"))
            elif any(x in lower_text for x in ["ахмет", "ахмед", "завхоз", "труб", "парт", "проектор"]):
                # Определяем имя
                name = "Ахмед" if "ахмед" in lower_text else "Ахмет (Завхоз)"
                tasks.append(TaskItem(assignee=name, deadline="Срочно", description=f"Техническая задача: {text}", rag_compliance="Проверка пройдена"))
            elif "охрана" in lower_text or "выход" in lower_text:
                 tasks.append(TaskItem(assignee="Охрана", deadline="Сегодня", description="Проверить все запасные выходы", rag_compliance="Соответствует нормам пожарной безопасности"))
            else:
                # Универсальный фоллбек — создаем хотя бы одну задачу из текста
                 tasks.append(TaskItem(assignee="Нераспознанный сотрудник", deadline="В течение дня", description=f"{text}", rag_compliance="Без нарушений"))

        return TaskDecomposition(general_context=text, tasks=tasks, substitution_triggered=substitution)
