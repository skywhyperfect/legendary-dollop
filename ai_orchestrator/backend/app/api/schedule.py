from fastapi import APIRouter, Response, Body
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import pandas as pd
import os
import tempfile
from app.services.scheduler import find_substitution
from app.services.legal_generator import generate_substitution_order
from app.services.pdf_service import create_order_html
from app.data_loader import load_staff, load_schedule 
from app.services.generator import generate_weekly_schedule, generate_all_staff_schedules

router = APIRouter()

class ClassLoadConstraint(BaseModel):
    class_name: str
    subject_hours: Dict[str, int]

class TeacherConstraint(BaseModel):
    teacher_name: str
    max_hours: Optional[int] = None
    subjects: Optional[List[str]] = None
    unavailable: Optional[List[Dict[str, int]]] = None

class RoomConstraint(BaseModel):
    room_name: str
    capacity: Optional[int] = None
    types: Optional[List[str]] = None
    unavailable: Optional[List[Dict[str, int]]] = None

class ScheduleConstraints(BaseModel):
    class_load: Optional[List[ClassLoadConstraint]] = None
    teacher_constraints: Optional[List[TeacherConstraint]] = None
    room_constraints: Optional[List[RoomConstraint]] = None

class ScheduleTarget(BaseModel):
    classes: Optional[List[str]] = None
    constraints: Optional[ScheduleConstraints] = None

import re
from openpyxl.styles import Alignment, PatternFill, Font

class ScheduleExportData(BaseModel):
    schedule: List[dict]

@router.post("/download-excel")
async def export_excel(data: ScheduleExportData):
    """
    Принимает JSON сгенерённого расписания и отдаёт "Ленточное расписание"
    Сгруппировано по Параллелям и Дням недели, в формате Pivot-матрицы.
    """
    df = pd.DataFrame(data.schedule)
    tmp_path = os.path.join(tempfile.gettempdir(), f"ribbon_schedule_{int(datetime.now().timestamp())}.xlsx")
    
    if df.empty:
        df.to_excel(tmp_path, index=False, engine='openpyxl')
    else:
        # 1. Извлекаем параллель
        def get_grade(x):
            match = re.search(r'\d+', str(x))
            return int(match.group()) if match else 0
            
        df['Grade'] = df['Класс'].apply(get_grade)
        
        # 2. Формируем содержимое ячейки с переносом строк
        df['Cell'] = df['Предмет'] + "\n" + df['Учитель'] + "\n(" + df['Кабинет'] + ")"
        
        with pd.ExcelWriter(tmp_path, engine='openpyxl') as writer:
            grades_list = sorted(df['Grade'].unique())
            days_order = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
            
            for grade in grades_list:
                for day in days_order:
                    subset = df[(df['Grade'] == grade) & (df['День'] == day)]
                    if subset.empty:
                        continue
                        
                    # Разворачиваем Ленту (Pivot)
                    pivot = subset.pivot(index='Урок', columns='Класс', values='Cell')
                    
                    # Фиксируем порядок строк (уроки с 1 до 6)
                    pivot = pivot.reindex(list(range(1, 7)))
                    
                    # Имя вкладки (макс 31 символ в Excel) e.g., "10кл Пн"
                    day_short = day[:2]
                    sheet_name = f"{grade} кл. {day_short}"
                    pivot.to_excel(writer, sheet_name=sheet_name)
                    
                    # --- КРАСИВОЕ ФОРМАТИРОВАНИЕ OpenPyXL ---
                    worksheet = writer.sheets[sheet_name]
                    
                    header_fill = PatternFill(start_color="3B82F6", end_color="3B82F6", fill_type="solid") # Tailwind Blue 500
                    header_font = Font(color="FFFFFF", bold=True)
                    index_fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid") # Tailwind Blue 50
                    
                    for col in worksheet.columns:
                        col_letter = col[0].column_letter
                        worksheet.column_dimensions[col_letter].width = 26
                        
                        for cell in col:
                            cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
                            
                            # Форматируем шапку (Классы)
                            if cell.row == 1:
                                cell.fill = header_fill
                                cell.font = header_font
                            
                            # Форматируем боковик (Уроки)
                            if cell.column == 1 and cell.row > 1:
                                cell.fill = index_fill
                                cell.font = Font(bold=True, color="1E3A8A")
                                
                    # Высота строк для переноса
                    for row in range(2, 9):
                        worksheet.row_dimensions[row].height = 65

    return FileResponse(
        tmp_path, 
        filename="Покойо_Ленточное_Расписание.xlsx", 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/generate-schedule")
async def api_generate_schedule(target: ScheduleTarget):
    """
    Генерирует расписание на неделю с нуля.
    Классы передаются в body: {"classes": ["1А", "5Б"], "constraints": {...}}.
    Результат возвращается в виде JSON-списка.
    """
    schedule = generate_weekly_schedule(target.classes, target.constraints.dict() if target.constraints else None)
    return {"status": "success", "total_slots": len(schedule), "schedule": schedule}

@router.get("/staff-schedule")
async def api_get_staff_schedule():
    """
    Возвращает персонализированное расписание для администрации и техперсонала.
    Включает задачи, спарсенные из WhatsApp.
    """
    from app.services.generator import generate_staff_schedule
    staff_sched = generate_staff_schedule()
    return {"status": "success", "schedule": staff_sched}

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

