from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.services.scheduler import find_substitution
from app.services.legal_generator import generate_substitution_order
from app.services.pdf_service import create_order_html
from app.data_loader import load_staff, load_schedule

router = APIRouter()

@router.get("/teacher-profile")
async def get_teacher_profile(teacher_name: str = "Иванова И. И."):
    """Mock-профиль учителя, берет реальные данные из Excel"""
    try:
        staff = load_staff()
        schedule = load_schedule()

        # Find teacher
        teacher_info = next((t for t in staff if teacher_name.lower() in t.get("ФИО", "").lower()), None)
        if not teacher_info and staff:
            # Fallback to first teacher if not found
            teacher_info = staff[0]
            teacher_name = teacher_info.get("ФИО", "Неизвестно")

        # Find schedule for today (Monday mock)
        today_val = "Понедельник"
        tsched = [s for s in schedule if s.get("Учитель") == teacher_name and s.get("День") == today_val]
        
        # Format schedule
        formatted_sched = []
        for s in sorted(tsched, key=lambda x: str(x.get("Урок"))):
            lesson_num = s.get("Урок")
            time_map = {1: "08:00", 2: "08:45", 3: "09:40", 4: "10:35", 5: "11:30", 6: "12:25"}
            formatted_sched.append({
                "time": time_map.get(lesson_num, f"Урок {lesson_num}"),
                "subject": s.get("Предмет", "-"),
                "class_name": s.get("Класс", "-"),
                "room": s.get("Кабинет", "-"),
                "is_substitution": False
            })

        return {
            "name": teacher_name,
            "role": teacher_info.get("Должность", "Учитель") if teacher_info else "Учитель",
            "schedule": formatted_sched,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"name": "Ошибка загрузки", "role": "Учитель", "schedule": []}

class SubstitutionRequest(BaseModel):
    teacher_name: str
    date: Optional[str] = None

class OrderGenerationRequest(BaseModel):
    missing_teacher: str
    substitute_teacher: str
    lesson_number: int
    class_name: str
    room: str

@router.post("/substitute")
async def schedule_substitute(req: SubstitutionRequest):
    plan = find_substitution(req.teacher_name, req.date)
    return {"substitution_plan": plan}

@router.post("/generate-order")
async def generate_order(req: OrderGenerationRequest):
    order = generate_substitution_order(
        req.missing_teacher,
        req.substitute_teacher,
        req.lesson_number,
        req.class_name,
        req.room
    )
    return order

@router.post("/generate-order-pdf")
async def generate_order_pdf(req: OrderGenerationRequest):
    order = generate_substitution_order(
        req.missing_teacher,
        req.substitute_teacher,
        req.lesson_number,
        req.class_name,
        req.room
    )

    current_date = datetime.now().strftime("%d.%m.%Y")

    html_content = create_order_html(
        missing_teacher=req.missing_teacher,
        substitute_teacher=req.substitute_teacher,
        lesson_number=req.lesson_number,
        class_name=req.class_name,
        room=req.room,
        order_date=current_date,
        order_number=f"78-{req.lesson_number}",
        ai_preamble=order.preamble,
        ai_body=order.order_body_ru,
        ai_body_kz=order.order_body_kz,
    )

    return HTMLResponse(content=html_content, status_code=200)

