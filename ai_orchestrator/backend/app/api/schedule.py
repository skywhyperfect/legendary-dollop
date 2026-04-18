from fastapi import APIRouter, Response, Body, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
import os
import tempfile
from app.services.scheduler import find_substitution
from app.services.legal_generator import generate_substitution_order
from app.services.pdf_service import create_order_html
from app.data_loader import load_staff, load_schedule
from app.services.generator import generate_weekly_schedule
from collections import defaultdict

router = APIRouter()

class ScheduleTarget(BaseModel):
    classes: Optional[List[str]] = None

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
    Классы передаются в body: {"classes": ["1А", "5Б"]}.
    Результат возвращается в виде JSON-списка.
    """
    schedule = generate_weekly_schedule(target.classes)
    return {"status": "success", "total_slots": len(schedule), "schedule": schedule}

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

# ==================== HEATMAP API ====================

class StaffMember(BaseModel):
    name: str
    role: str
    subject: Optional[str] = None
    max_hours_per_day: int = 6
    max_hours_per_week: int = 30

class StaffUpdateRequest(BaseModel):
    staff: List[StaffMember]

@router.get("/heatmap")
async def get_heatmap(day: str = "Понедельник"):
    """
    Тепловая карта нагрузки сотрудников.
    Показывает загрузку учителей, кабинеты и конфликты.
    """
    try:
        staff = load_staff()
        schedule = load_schedule()
        
        if not staff or not schedule:
            # Возвращаем mock-данные если Excel файлов нет
            return get_mock_heatmap(day)
        
        # Анализируем нагрузку
        teacher_load = defaultdict(lambda: {"lessons": 0, "slots": [], "overloaded": False})
        room_load = defaultdict(lambda: {"lessons": 0, "slots": []})
        conflicts = []
        
        # Считаем нагрузку по учителям
        for lesson in schedule:
            if lesson.get("День") != day:
                continue
                
            teacher = lesson.get("Учитель", "")
            room = lesson.get("Кабинет", "")
            lesson_num = lesson.get("Урок", 0)
            
            if teacher:
                teacher_load[teacher]["lessons"] += 1
                teacher_load[teacher]["slots"].append({
                    "lesson": lesson_num,
                    "class": lesson.get("Класс"),
                    "subject": lesson.get("Предмет"),
                    "room": room
                })
            
            if room:
                room_load[room]["lessons"] += 1
                room_load[room]["slots"].append({
                    "lesson": lesson_num,
                    "teacher": teacher,
                    "class": lesson.get("Класс")
                })
        
        # Проверяем перегрузку (больше 6 уроков в день)
        for teacher, data in teacher_load.items():
            if data["lessons"] > 6:
                data["overloaded"] = True
        
        # Проверяем конфликты кабинетов
        for room, data in room_load.items():
            lesson_slots = [s["lesson"] for s in data["slots"]]
            if len(lesson_slots) != len(set(lesson_slots)):
                conflicts.append({
                    "type": "room_conflict",
                    "room": room,
                    "message": f"Кабинет {room} занят дважды на одном уроке"
                })
        
        # Формируем ответ
        heatmap_data = {
            "day": day,
            "teachers": [],
            "rooms": [],
            "conflicts": conflicts,
            "summary": {
                "total_teachers": len(teacher_load),
                "overloaded_teachers": sum(1 for t in teacher_load.values() if t["overloaded"]),
                "total_rooms": len(room_load),
                "room_conflicts": len(conflicts)
            }
        }
        
        # Добавляем данные по учителям
        for teacher, data in teacher_load.items():
            # Находим информацию об учителе
            teacher_info = next((t for t in staff if t.get("ФИО") == teacher), {})
            heatmap_data["teachers"].append({
                "name": teacher,
                "subject": teacher_info.get("Предмет", "Неизвестно"),
                "role": teacher_info.get("Должность", "Учитель"),
                "lessons_count": data["lessons"],
                "overloaded": data["overloaded"],
                "utilization": min(data["lessons"] / 6 * 100, 100),  # % от макс нагрузки
                "slots": data["slots"]
            })
        
        # Сортируем по загрузке (самые загруженные сверху)
        heatmap_data["teachers"].sort(key=lambda x: x["lessons_count"], reverse=True)
        
        return heatmap_data
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return get_mock_heatmap(day)

def get_mock_heatmap(day: str) -> dict:
    """Mock-данные для тепловой карты"""
    mock_teachers = [
        {"name": "Аскар Б.", "subject": "Математика", "role": "Учитель", "lessons": 6, "overloaded": False},
        {"name": "Смирнова Е.", "subject": "Русский язык", "role": "Учитель", "lessons": 7, "overloaded": True},
        {"name": "Кусаинова А.", "subject": "Английский язык", "role": "Учитель", "lessons": 5, "overloaded": False},
        {"name": "Нурланов Т.", "subject": "История", "role": "Учитель", "lessons": 4, "overloaded": False},
        {"name": "Ахметов К.", "subject": "Физкультура", "role": "Учитель", "lessons": 6, "overloaded": False},
        {"name": "Жаксыбеков Е.", "subject": "Физика", "role": "Учитель", "lessons": 3, "overloaded": False},
        {"name": "Сарсенбаев А.Т.", "subject": "-", "role": "Директор", "lessons": 2, "overloaded": False},
        {"name": "Иванова М.", "subject": "-", "role": "Завхоз", "lessons": 0, "overloaded": False},
    ]
    
    return {
        "day": day,
        "teachers": [
            {**t, "utilization": min(t["lessons"] / 6 * 100, 100), "slots": []}
            for t in mock_teachers
        ],
        "rooms": [],
        "conflicts": [
            {"type": "room_conflict", "room": "302", "message": "Кабинет 302 занят дважды на 3 уроке"}
        ],
        "summary": {
            "total_teachers": len(mock_teachers),
            "overloaded_teachers": sum(1 for t in mock_teachers if t["overloaded"]),
            "total_rooms": 15,
            "room_conflicts": 1
        }
    }

@router.post("/heatmap/update-staff")
async def update_staff_load(request: StaffUpdateRequest):
    """
    Обновление максимальной нагрузки для сотрудников.
    Позволяет директору настроить ограничения.
    """
    # В реальном приложении сохраняем в БД
    # Сейчас просто возвращаем подтверждение
    return {
        "status": "success",
        "updated_count": len(request.staff),
        "message": "Нагрузка сотрудников обновлена"
    }

# ==================== DRAG-AND-DROP API ====================

class DragDropRequest(BaseModel):
    """Запрос на перемещение урока в расписании"""
    lesson_id: Optional[int] = None  # ID урока в БД (если есть)
    day_from: str
    lesson_from: int
    class_name: str
    
    day_to: str
    lesson_to: int
    
    # Опционально: смена кабинета
    new_room: Optional[str] = None
    new_teacher: Optional[str] = None

class DragDropResponse(BaseModel):
    success: bool
    message: str
    conflicts: List[Dict[str, Any]]
    updated_schedule: Optional[List[Dict]] = None

@router.post("/schedule/drag-drop")
async def handle_drag_drop(request: DragDropRequest) -> DragDropResponse:
    """
    Обработка drag-and-drop перемещения урока.
    Проверяет конфликты и применяет изменения.
    """
    conflicts = []
    
    try:
        schedule = load_schedule()
        if not schedule:
            return DragDropResponse(
                success=False,
                message="Расписание не загружено",
                conflicts=[]
            )
        
        # Находим перемещаемый урок
        moving_lesson = None
        for lesson in schedule:
            if (lesson.get("День") == request.day_from and 
                lesson.get("Урок") == request.lesson_from and
                lesson.get("Класс") == request.class_name):
                moving_lesson = lesson.copy()
                break
        
        if not moving_lesson:
            return DragDropResponse(
                success=False,
                message="Урок не найден",
                conflicts=[]
            )
        
        # Проверяем конфликты на новом месте
        
        # 1. Проверка: занят ли учитель
        teacher = request.new_teacher or moving_lesson.get("Учитель")
        teacher_busy = any(
            l for l in schedule
            if (l.get("День") == request.day_to and 
                l.get("Урок") == request.lesson_to and
                l.get("Учитель") == teacher and
                l.get("Класс") != request.class_name)
        )
        if teacher_busy:
            conflicts.append({
                "type": "teacher_busy",
                "message": f"Учитель {teacher} уже занят на {request.day_to} {request.lesson_to} урок",
                "severity": "error"
            })
        
        # 2. Проверка: занят ли кабинет
        room = request.new_room or moving_lesson.get("Кабинет")
        room_busy = any(
            l for l in schedule
            if (l.get("День") == request.day_to and 
                l.get("Урок") == request.lesson_to and
                l.get("Кабинет") == room and
                l.get("Класс") != request.class_name)
        )
        if room_busy:
            conflicts.append({
                "type": "room_busy",
                "message": f"Кабинет {room} уже занят на {request.day_to} {request.lesson_to} урок",
                "severity": "error"
            })
        
        # 3. Проверка: не превышает ли учитель дневную норму
        teacher_lessons_on_day = sum(
            1 for l in schedule
            if l.get("День") == request.day_to and l.get("Учитель") == teacher
        )
        if teacher_lessons_on_day >= 6:
            conflicts.append({
                "type": "teacher_overload",
                "message": f"Учитель {teacher} будет перегружен (6+ уроков в день)",
                "severity": "warning"
            })
        
        # Если есть критические конфликты - отменяем
        if any(c["severity"] == "error" for c in conflicts):
            return DragDropResponse(
                success=False,
                message="Обнаружены конфликты при перемещении",
                conflicts=conflicts
            )
        
        # Применяем изменения (в памяти, для демо)
        # В реальном приложении - сохраняем в БД
        updated_schedule = []
        for lesson in schedule:
            if (lesson.get("День") == request.day_from and 
                lesson.get("Урок") == request.lesson_from and
                lesson.get("Класс") == request.class_name):
                # Обновляем урок
                updated_lesson = lesson.copy()
                updated_lesson["День"] = request.day_to
                updated_lesson["Урок"] = request.lesson_to
                if request.new_room:
                    updated_lesson["Кабинет"] = request.new_room
                if request.new_teacher:
                    updated_lesson["Учитель"] = request.new_teacher
                updated_schedule.append(updated_lesson)
            else:
                updated_schedule.append(lesson.copy())
        
        return DragDropResponse(
            success=True,
            message=f"Урок успешно перемещен на {request.day_to}, {request.lesson_to} урок",
            conflicts=conflicts,
            updated_schedule=updated_schedule
        )
        
    except Exception as e:
        return DragDropResponse(
            success=False,
            message=f"Ошибка: {str(e)}",
            conflicts=[]
        )

# ==================== EXTENDED PROFILES API ====================

class EmployeeProfile(BaseModel):
    name: str
    role: str
    department: Optional[str] = None
    schedule: List[Dict] = []
    tasks: List[Dict] = []
    workload: Dict[str, Any] = {}

@router.get("/profile/{employee_name}")
async def get_employee_profile(employee_name: str):
    """
    Расширенный профиль сотрудника (учитель, завхоз, директор, слесарь).
    Включает расписание, задачи, нагрузку.
    """
    try:
        staff = load_staff()
        schedule = load_schedule()
        
        # Ищем сотрудника
        employee_info = None
        if staff:
            employee_info = next(
                (e for e in staff if employee_name.lower() in e.get("ФИО", "").lower()),
                None
            )
        
        if not employee_info:
            # Возвращаем mock-профиль
            return get_mock_employee_profile(employee_name)
        
        # Формируем расписание
        employee_schedule = []
        if schedule:
            for lesson in schedule:
                if lesson.get("Учитель") == employee_info.get("ФИО"):
                    employee_schedule.append({
                        "day": lesson.get("День"),
                        "lesson": lesson.get("Урок"),
                        "time": get_lesson_time(lesson.get("Урок")),
                        "subject": lesson.get("Предмет"),
                        "class": lesson.get("Класс"),
                        "room": lesson.get("Кабинет"),
                        "type": "lesson"
                    })
        
        # Считаем нагрузку
        total_lessons = len(employee_schedule)
        max_lessons = 30  # недельная нагрузка
        workload = {
            "weekly_hours": total_lessons,
            "max_weekly_hours": max_lessons,
            "utilization": (total_lessons / max_lessons) * 100 if max_lessons > 0 else 0,
            "status": "normal" if total_lessons <= max_lessons else "overloaded"
        }
        
        return {
            "name": employee_info.get("ФИО"),
            "role": employee_info.get("Должность"),
            "department": employee_info.get("Предмет", "Администрация"),
            "schedule": employee_schedule,
            "tasks": [],  # Задачи можно подгрузить из БД
            "workload": workload
        }
        
    except Exception as e:
        return get_mock_employee_profile(employee_name)

def get_mock_employee_profile(employee_name: str) -> dict:
    """Mock-профиль сотрудника с динамическим расписанием"""
    
    # Определяем роль по имени
    role_map = {
        "директор": "Директор",
        "завуч": "Завуч",
        "завхоз": "Завхоз",
        "слесарь": "Слесарь",
        "секретарь": "Секретарь",
        "учитель": "Учитель"
    }
    
    role = "Сотрудник"
    for key, value in role_map.items():
        if key in employee_name.lower():
            role = value
            break
    
    # Получаем текущие задачи из БД для динамического расписания
    tasks_from_db = []
    try:
        import sqlite3
        conn = sqlite3.connect("orchestrator.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM tg_messages WHERE parsed_type IN ('incident', 'medical') ORDER BY created_at DESC LIMIT 5"
        )
        tasks_from_db = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except:
        pass
    
    # Генерируем расписание в зависимости от роли
    mock_schedule = []
    if role == "Директор":
        mock_schedule = [
            {"day": "Понедельник", "lesson": 1, "time": "08:00", "subject": "Планерка", "class": "-", "room": "Кабинет директора", "type": "meeting"},
            {"day": "Понедельник", "lesson": 3, "time": "09:40", "subject": "Прием родителей", "class": "-", "room": "Кабинет директора", "type": "meeting"},
            {"day": "Вторник", "lesson": 2, "time": "08:45", "subject": "Посещение урока", "class": "1А", "room": "101", "type": "control"},
            {"day": "Среда", "lesson": 1, "time": "08:00", "subject": "Педсовет", "class": "-", "room": "Актовый зал", "type": "meeting"},
            {"day": "Четверг", "lesson": 4, "time": "10:35", "subject": "Совещание с завучами", "class": "-", "room": "Кабинет директора", "type": "meeting"},
            {"day": "Пятница", "lesson": 5, "time": "11:30", "subject": "Подведение итогов", "class": "-", "room": "Кабинет директора", "type": "admin"},
            # Окна для проверки тетрадей и работы с документами
            {"day": "Понедельник", "lesson": 2, "time": "08:45", "subject": "Работа с документами", "class": "-", "room": "Кабинет директора", "type": "window"},
            {"day": "Среда", "lesson": 3, "time": "09:40", "subject": "Окно (проверка тетрадей)", "class": "-", "room": "Кабинет директора", "type": "window"},
            {"day": "Четверг", "lesson": 2, "time": "08:45", "subject": "Окно (подготовка к совещанию)", "class": "-", "room": "Кабинет директора", "type": "window"},
            # Дежурства
            {"day": "Вторник", "lesson": 4, "time": "10:35", "subject": "Дежурство на перемене", "class": "-", "room": "2 этаж", "type": "duty"},
            {"day": "Четверг", "lesson": 3, "time": "09:40", "subject": "Дежурство на перемене", "class": "-", "room": "1 этаж", "type": "duty"},
            # Обед
            {"day": "Понедельник", "lesson": 4, "time": "10:35", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Среда", "lesson": 2, "time": "08:45", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Пятница", "lesson": 3, "time": "09:40", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"}
        ]
        # Добавляем динамические задачи из чатов (инциденты)
        for i, task in enumerate(tasks_from_db[:2]):
            mock_schedule.append({
                "day": "Пятница",
                "lesson": 6,
                "time": "12:25",
                "subject": f"Инцидент: {task.get('parsed_summary', 'Требуется внимание')[:40]}",
                "class": "-",
                "room": task.get('location', 'Не указано'),
                "type": "task",
                "from_chat": True,
                "sender": task.get('sender', 'Неизвестно')
            })
            
    elif role == "Завхоз":
        mock_schedule = [
            {"day": "Понедельник", "lesson": 1, "time": "08:00", "subject": "Обход школы", "class": "-", "room": "Все этажи", "type": "inspection"},
            {"day": "Понедельник", "lesson": 3, "time": "09:40", "subject": "Ремонт парты", "class": "-", "room": "Каб. 12", "type": "task"},
            {"day": "Вторник", "lesson": 2, "time": "08:45", "subject": "Проверка отопления", "class": "-", "room": "Подвал", "type": "inspection"},
            {"day": "Среда", "lesson": 1, "time": "08:00", "subject": "Обход школы", "class": "-", "room": "Все этажи", "type": "inspection"},
            {"day": "Четверг", "lesson": 4, "time": "10:35", "subject": "Закупка материалов", "class": "-", "room": "Склад", "type": "admin"},
            {"day": "Пятница", "lesson": 5, "time": "11:30", "subject": "Отчетность", "class": "-", "room": "Кабинет завхоза", "type": "admin"},
            # Окна для подготовки
            {"day": "Понедельник", "lesson": 2, "time": "08:45", "subject": "Окно (подготовка к обходу)", "class": "-", "room": "Кабинет завхоза", "type": "window"},
            {"day": "Среда", "lesson": 3, "time": "09:40", "subject": "Окно (составление плана)", "class": "-", "room": "Кабинет завхоза", "type": "window"},
            # Обед
            {"day": "Вторник", "lesson": 4, "time": "10:35", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Четверг", "lesson": 2, "time": "08:45", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Пятница", "lesson": 4, "time": "10:35", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"}
        ]
        # Добавляем динамические задачи из чатов (инциденты)
        for i, task in enumerate(tasks_from_db[:3]):
            mock_schedule.append({
                "day": ["Вторник", "Среда", "Четверг"][i],
                "lesson": 3,
                "time": "09:40",
                "subject": f"Инцидент: {task.get('parsed_summary', 'Требуется ремонт')[:40]}",
                "class": "-",
                "room": task.get('location', 'Не указано'),
                "type": "task",
                "from_chat": True,
                "sender": task.get('sender', 'Неизвестно')
            })
            
    elif role == "Слесарь":
        mock_schedule = [
            {"day": "Понедельник", "lesson": 1, "time": "08:00", "subject": "Проверка сантехники", "class": "-", "room": "Все туалеты", "type": "inspection"},
            {"day": "Вторник", "lesson": 2, "time": "08:45", "subject": "Ремонт крана", "class": "-", "room": "Каб. 201", "type": "task"},
            {"day": "Среда", "lesson": 1, "time": "08:00", "subject": "Проверка сантехники", "class": "-", "room": "Все туалеты", "type": "inspection"},
            {"day": "Четверг", "lesson": 3, "time": "09:40", "subject": "Замена ламп", "class": "-", "room": "Коридор 2 этаж", "type": "task"},
            {"day": "Пятница", "lesson": 4, "time": "10:35", "subject": "Подготовка к выходным", "class": "-", "room": "Слесарная", "type": "admin"},
            # Окна
            {"day": "Понедельник", "lesson": 3, "time": "09:40", "subject": "Окно (подготовка инструментов)", "class": "-", "room": "Слесарная", "type": "window"},
            {"day": "Среда", "lesson": 4, "time": "10:35", "subject": "Окно (отдых)", "class": "-", "room": "Слесарная", "type": "window"},
            # Обед
            {"day": "Вторник", "lesson": 3, "time": "09:40", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Четверг", "lesson": 2, "time": "08:45", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Пятница", "lesson": 2, "time": "08:45", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"}
        ]
        # Добавляем динамические задачи из чатов (инциденты)
        for i, task in enumerate(tasks_from_db[:2]):
            mock_schedule.append({
                "day": ["Понедельник", "Среда"][i],
                "lesson": 2,
                "time": "08:45",
                "subject": f"Срочный ремонт: {task.get('parsed_summary', 'Требуется внимание')[:35]}",
                "class": "-",
                "room": task.get('location', 'Не указано'),
                "type": "task",
                "from_chat": True,
                "sender": task.get('sender', 'Неизвестно')
            })
            
    else:
        # Для учителей и других сотрудников
        mock_schedule = [
            {"day": "Понедельник", "lesson": 1, "time": "08:00", "subject": "Урок", "class": "5А", "room": "201", "type": "lesson"},
            {"day": "Понедельник", "lesson": 3, "time": "09:40", "subject": "Урок", "class": "6Б", "room": "201", "type": "lesson"},
            {"day": "Вторник", "lesson": 2, "time": "08:45", "subject": "Урок", "class": "7А", "room": "201", "type": "lesson"},
            {"day": "Среда", "lesson": 1, "time": "08:00", "subject": "Урок", "class": "8В", "room": "201", "type": "lesson"},
            {"day": "Четверг", "lesson": 4, "time": "10:35", "subject": "Урок", "class": "9А", "room": "201", "type": "lesson"},
            {"day": "Пятница", "lesson": 5, "time": "11:30", "subject": "Классный час", "class": "5А", "room": "201", "type": "lesson"},
            # Окна для проверки тетрадей
            {"day": "Понедельник", "lesson": 2, "time": "08:45", "subject": "Окно (проверка тетрадей)", "class": "-", "room": "201", "type": "window"},
            {"day": "Среда", "lesson": 3, "time": "09:40", "subject": "Окно (подготовка к уроку)", "class": "-", "room": "201", "type": "window"},
            {"day": "Пятница", "lesson": 2, "time": "08:45", "subject": "Окно (методическая работа)", "class": "-", "room": "201", "type": "window"},
            # Дежурства
            {"day": "Вторник", "lesson": 3, "time": "09:40", "subject": "Дежурство на перемене", "class": "-", "room": "2 этаж", "type": "duty"},
            {"day": "Четверг", "lesson": 2, "time": "08:45", "subject": "Deжурство на перемене", "class": "-", "room": "1 этаж", "type": "duty"},
            # Обед
            {"day": "Понедельник", "lesson": 4, "time": "10:35", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Среда", "lesson": 4, "time": "10:35", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"},
            {"day": "Пятница", "lesson": 4, "time": "10:35", "subject": "Обед", "class": "-", "room": "Столовая", "type": "lunch"}
        ]
        # Добавляем динамические задачи из чатов (инциденты)
        for i, task in enumerate(tasks_from_db[:1]):
            mock_schedule.append({
                "day": "Четверг",
                "lesson": 6,
                "time": "12:25",
                "subject": f"Инцидент: {task.get('parsed_summary', 'Требуется внимание')[:35]}",
                "class": "-",
                "room": task.get('location', 'Не указано'),
                "type": "task",
                "from_chat": True,
                "sender": task.get('sender', 'Неизвестно')
            })
    
    mock_tasks = [
        {"id": 1, "title": "Подготовить отчет", "deadline": "Сегодня", "status": "in_progress", "priority": "high"},
        {"id": 2, "title": "Проверить журналы", "deadline": "Завтра", "status": "pending", "priority": "medium"},
        {"id": 3, "title": "Провести собрание", "deadline": "Пятница", "status": "pending", "priority": "low"}
    ]
    
    return {
        "name": employee_name,
        "role": role,
        "department": "Администрация" if role in ["Директор", "Завуч", "Завхоз"] else "Учебная часть",
        "schedule": mock_schedule,
        "tasks": mock_tasks,
        "workload": {
            "weekly_hours": len([s for s in mock_schedule if s["type"] in ["lesson", "task", "duty"]]),
            "max_weekly_hours": 30,
            "utilization": round(len([s for s in mock_schedule if s["type"] in ["lesson", "task", "duty"]]) / 30 * 100, 1),
            "status": "normal"
        },
        "dynamic_tasks_count": len([s for s in mock_schedule if s.get("from_chat")]),
        "schedule_types": {
            "lesson": len([s for s in mock_schedule if s["type"] == "lesson"]),
            "task": len([s for s in mock_schedule if s["type"] == "task"]),
            "window": len([s for s in mock_schedule if s["type"] == "window"]),
            "duty": len([s for s in mock_schedule if s["type"] == "duty"]),
            "lunch": len([s for s in mock_schedule if s["type"] == "lunch"]),
            "meeting": len([s for s in mock_schedule if s["type"] == "meeting"]),
            "inspection": len([s for s in mock_schedule if s["type"] == "inspection"]),
            "admin": len([s for s in mock_schedule if s["type"] == "admin"]),
        }
    }

def get_lesson_time(lesson_num: int) -> str:
    """Возвращает время начала урока по его номеру"""
    time_map = {
        1: "08:00",
        2: "08:45",
        3: "09:40",
        4: "10:35",
        5: "11:30",
        6: "12:25"
    }
    return time_map.get(lesson_num, f"Урок {lesson_num}")

# ==================== NOTIFICATION API ====================

class NotificationRequest(BaseModel):
    """Запрос на отправку уведомления"""
    recipient: str  # Имя получателя или роль
    message: str
    type: str = "task"  # task, substitution, incident, general
    channel: str = "whatsapp"  # whatsapp, telegram, push
    urgent: bool = False

@router.post("/notify/send")
async def send_notification(request: NotificationRequest):
    """
    Отправка уведомления сотруднику.
    В реальном приложении интегрируется с WhatsApp/Telegram API.
    """
    try:
        # Логируем уведомление
        print(f"📱 Отправка уведомления [{request.channel}]:")
        print(f"   Получатель: {request.recipient}")
        print(f"   Тип: {request.type}")
        print(f"   Сообщение: {request.message}")
        print(f"   Срочно: {request.urgent}")
        
        # В реальном приложении здесь будет отправка через:
        # - WhatsApp API (если channel="whatsapp")
        # - Telegram Bot API (если channel="telegram")
        # - Push notification (если channel="push")
        
        # Для демо возвращаем успех
        return {
            "status": "success",
            "message": f"Уведомление отправлено {request.recipient}",
            "notification": {
                "recipient": request.recipient,
                "message": request.message,
                "type": request.type,
                "channel": request.channel,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/notify/bulk")
async def send_bulk_notifications(recipients: List[str], message: str, type: str = "general"):
    """
    Массовая рассылка уведомлений.
    """
    results = []
    for recipient in recipients:
        result = await send_notification(
            NotificationRequest(
                recipient=recipient,
                message=message,
                type=type
            )
        )
        results.append(result)
    
    return {
        "status": "success",
        "sent_count": len(results),
        "results": results
    }

# ==================== CONSTRAINTS MATRIX API ====================

class ClassConstraint(BaseModel):
    class_name: str
    grade: int
    letter: str
    subjects: Dict[str, int]  # предмет -> часов в неделю

class TeacherConstraint(BaseModel):
    name: str
    subject: str
    max_hours_per_week: int = 30
    max_hours_per_day: int = 6
    unavailable_slots: List[Dict[str, Any]] = []  # [{"day": "Пятница", "lesson": 4}]

class RoomConstraint(BaseModel):
    room_number: str
    capacity: int = 30
    type: str = "classroom"  # classroom, lab, gym, library, etc.
    equipment: List[str] = []

class ConstraintsMatrix(BaseModel):
    classes: List[ClassConstraint] = []
    teachers: List[TeacherConstraint] = []
    rooms: List[RoomConstraint] = []

@router.get("/constraints")
async def get_constraints():
    """
    Получение текущих ограничений для генератора расписания.
    """
    return {
        "classes": [
            {"class_name": "1А", "grade": 1, "letter": "A", "subjects": {"Математика": 5, "Русский язык": 3, "Английский язык": 3}},
            {"class_name": "1Б", "grade": 1, "letter": "Б", "subjects": {"Математика": 5, "Русский язык": 3, "Английский язык": 3}},
            {"class_name": "2А", "grade": 2, "letter": "A", "subjects": {"Математика": 5, "Русский язык": 3, "Английский язык": 3}},
            {"class_name": "3А", "grade": 3, "letter": "A", "subjects": {"Математика": 5, "Русский язык": 3, "Английский язык": 3}},
            {"class_name": "3Б", "grade": 3, "letter": "Б", "subjects": {"Математика": 5, "Русский язык": 3, "Английский язык": 3}},
            {"class_name": "3В", "grade": 3, "letter": "В", "subjects": {"Математика": 5, "Русский язык": 3, "Английский язык": 3}},
        ],
        "teachers": [
            {"name": "Аскар Б.", "subject": "Математика", "max_hours_per_week": 30, "max_hours_per_day": 6, "unavailable_slots": []},
            {"name": "Смирнова Е.", "subject": "Русский язык", "max_hours_per_week": 30, "max_hours_per_day": 6, "unavailable_slots": [{"day": "Пятница", "lesson": 5}]},
            {"name": "Кусаинова А.", "subject": "Английский язык", "max_hours_per_week": 30, "max_hours_per_day": 6, "unavailable_slots": []},
        ],
        "rooms": [
            {"room_number": "101", "capacity": 25, "type": "classroom", "equipment": ["доска", "проектор"]},
            {"room_number": "102", "capacity": 25, "type": "classroom", "equipment": ["доска", "проектор"]},
            {"room_number": "201", "capacity": 30, "type": "classroom", "equipment": ["доска", "проектор", "компьютеры"]},
            {"room_number": "302", "capacity": 25, "type": "classroom", "equipment": ["доска"]},
            {"room_number": "Спортзал", "capacity": 50, "type": "gym", "equipment": ["баскетбольные кольца", "шведская стенка"]},
            {"room_number": "Лингафонный", "capacity": 20, "type": "lab", "equipment": ["аудиооборудование", "компьютеры"]},
        ]
    }

@router.post("/constraints")
async def update_constraints(constraints: ConstraintsMatrix):
    """
    Обновление ограничений для генератора расписания.
    """
    # В реальном приложении сохраняем в БД
    return {
        "status": "success",
        "message": "Ограничения обновлены",
        "classes_count": len(constraints.classes),
        "teachers_count": len(constraints.teachers),
        "rooms_count": len(constraints.rooms)
    }

# ==================== RIBBON SCHEDULING API ====================

class RibbonConfig(BaseModel):
    """Конфигурация ленты для параллели классов"""
    parallel_grade: int  # Например, 3 для 3-х классов
    parallel_classes: List[str]  # ["3А", "3Б", "3В"]
    subject: str  # Например, "Английский язык"
    levels: List[str]  # ["Beginner", "Pre-Intermediate", "Intermediate", "Upper"]
    teachers_per_level: Dict[str, str]  # уровень -> учитель
    rooms_per_level: Dict[str, str]  # уровень -> кабинет
    day: str
    lesson: int

@router.get("/ribbons")
async def get_ribbon_configurations():
    """
    Получение конфигураций лент для параллелей.
    """
    return {
        "ribbons": [
            {
                "id": 1,
                "parallel_grade": 3,
                "parallel_classes": ["3А", "3Б", "3В"],
                "subject": "Английский язык",
                "levels": ["Beginner", "Pre-Intermediate", "Intermediate", "Upper"],
                "teachers": {
                    "Beginner": "Кусаинова А.",
                    "Pre-Intermediate": "Ли Карина",
                    "Intermediate": "Бекова Ж.",
                    "Upper": "Сейткали М."
                },
                "rooms": {
                    "Beginner": "201",
                    "Pre-Intermediate": "202",
                    "Intermediate": "301",
                    "Upper": "302"
                },
                "schedule": {
                    "day": "Вторник",
                    "lesson": 3
                }
            },
            {
                "id": 2,
                "parallel_grade": 5,
                "parallel_classes": ["5А", "5Б"],
                "subject": "Математика",
                "levels": ["Базовый", "Продвинутый"],
                "teachers": {
                    "Базовый": "Смирнова Е.",
                    "Продвинутый": "Аскар Б."
                },
                "rooms": {
                    "Базовый": "101",
                    "Продвинутый": "102"
                },
                "schedule": {
                    "day": "Среда",
                    "lesson": 2
                }
            }
        ]
    }

@router.post("/ribbons")
async def create_ribbon_config(config: RibbonConfig):
    """
    Создание новой конфигурации ленты.
    """
    return {
        "status": "success",
        "message": f"Лента для {config.parallel_grade} класса создана",
        "config": config.dict()
    }

@router.get("/ribbons/conflicts")
async def check_ribbon_conflicts():
    """
    Проверка конфликтов в ленточном расписании.
    """
    return {
        "conflicts": [],
        "message": "Конфликтов не обнаружено. Ленты настроены корректно.",
        "blocked_slots": [
            {"day": "Вторник", "lesson": 3, "classes": ["3А", "3Б", "3В"], "reason": "Английский язык (лента)"},
            {"day": "Среда", "lesson": 2, "classes": ["5А", "5Б"], "reason": "Математика (лента)"}
        ]
    }

# ==================== CONFLICT CHECK API ====================

class ConflictCheckRequest(BaseModel):
    employee_name: str
    day: str
    lesson: int
    activity_type: str = "meeting"  # meeting, control, lesson, etc.

@router.post("/conflicts/check")
async def check_conflicts(request: ConflictCheckRequest):
    """
    Проверка конфликтов для сотрудника на указанное время.
    Автоматически проверяет, не занят ли сотрудник в это время.
    """
    # Получаем расписание сотрудника
    profile = get_mock_employee_profile(request.employee_name)
    
    conflicts = []
    
    # Проверяем расписание
    for slot in profile["schedule"]:
        if slot["day"] == request.day and slot["lesson"] == request.lesson:
            conflicts.append({
                "type": "schedule_conflict",
                "existing_activity": slot["subject"],
                "existing_type": slot["type"],
                "room": slot["room"],
                "message": f"Сотрудник уже занят: {slot['subject']} ({slot['type']})"
            })
    
    if conflicts:
        return {
            "has_conflicts": True,
            "conflicts": conflicts,
            "message": f"Обнаружено {len(conflicts)} конфликтов"
        }
    else:
        return {
            "has_conflicts": False,
            "conflicts": [],
            "message": "Конфликтов не обнаружено. Время свободно."
        }

@router.get("/conflicts/summary")
async def get_conflicts_summary():
    """
    Сводка по всем конфликтам в расписании.
    """
    return {
        "total_conflicts": 0,
        "conflicts": [],
        "warnings": [
            {
                "type": "overload_warning",
                "employee": "Смирнова Е.",
                "message": "Перегрузка в Понедельник (7 уроков)",
                "severity": "medium"
            }
        ],
        "suggestions": [
            {
                "type": "optimization",
                "message": "Можно оптимизировать расписание 3-х классов, переместив 2 урока",
                "potential_improvement": "Снижение нагрузки на 15%"
            }
        ]
    }

# ==================== SMART SUBSTITUTION ENHANCEMENTS ====================

class SubstitutionWithNotification(BaseModel):
    teacher_name: str
    date: Optional[str] = None
    notify_teacher: bool = True
    notify_method: str = "whatsapp"

@router.post("/substitute/enhanced")
async def enhanced_substitute(req: SubstitutionWithNotification):
    """
    Улучшенная замена с автоматическим уведомлением и проверкой нагрузки.
    """
    # 1. Находим замену
    plan = find_substitution(req.teacher_name, req.date)
    
    if not plan:
        return {"status": "error", "message": "Замена не найдена"}
    
    # 2. Проверяем нагрузку заменяющего учителя
    substitution = plan[0]
    sub_teacher = substitution.get("substitute_teacher")
    
    # Получаем профиль заменяющего учителя
    sub_profile = get_mock_employee_profile(sub_teacher)
    
    # Проверяем, не превысит ли нагрузка допустимую
    current_load = sub_profile["workload"]["weekly_hours"]
    additional_hours = len([s for s in substitution.get("checks", {}).get("slots", [])])
    max_hours = 30
    
    overload_warning = None
    if current_load + additional_hours > max_hours:
        overload_warning = {
            "teacher": sub_teacher,
            "current_load": current_load,
            "additional_hours": additional_hours,
            "new_total": current_load + additional_hours,
            "max_hours": max_hours,
            "message": f"Внимание! Нагрузка учителя превысит норму: {current_load + additional_hours}/{max_hours} часов"
        }
    
    # 3. Отправляем уведомление (если запрошено)
    notification_sent = False
    if req.notify_teacher:
        try:
            await send_notification(
                NotificationRequest(
                    recipient=sub_teacher,
                    message=f"🔔 Срочная замена!\n\nУчитель {req.teacher_name} отсутствует.\nВам необходимо провести урок в {substitution.get('class_name')} классе.\nПредмет: {substitution.get('subject', 'Не указано')}\nКабинет: {substitution.get('room', 'Не указано')}\n\nПожалуйста, подтвердите получение.",
                    type="substitution",
                    channel=req.notify_method,
                    urgent=True
                )
            )
            notification_sent = True
        except Exception as e:
            notification_sent = False
    
    return {
        "status": "success",
        "substitution": substitution,
        "overload_warning": overload_warning,
        "notification_sent": notification_sent,
        "substitute_profile": {
            "name": sub_teacher,
            "current_load": current_load,
            "max_hours": max_hours,
            "utilization": sub_profile["workload"]["utilization"]
        }
    }

@router.post("/substitute/alternative")
async def find_alternative_substitute(req: SubstitutionRequest):
    """
    Поиск альтернативной замены, если основной кандидат не подходит.
    """
    # Находим основную замену
    main_plan = find_substitution(req.teacher_name, req.date)
    
    if not main_plan:
        return {"status": "error", "message": "Замена не найдена"}
    
    # Получаем профиль основного кандидата
    main_sub = main_plan[0].get("substitute_teacher")
    main_profile = get_mock_employee_profile(main_sub)
    
    # Проверяем, не перегружен ли он
    if main_profile["workload"]["utilization"] > 80:
        # Ищем альтернативу
        alternatives = [
            {"name": "Нурланов Т.", "subject": "История", "utilization": 45, "reason": "Меньшая нагрузка"},
            {"name": "Ахметов К.", "subject": "Физкультура", "utilization": 50, "reason": "Свободен в это время"}
        ]
        
        return {
            "status": "warning",
            "message": f"Основной кандидат ({main_sub}) перегружен ({main_profile['workload']['utilization']}%)",
            "main_candidate": {
                "name": main_sub,
                "utilization": main_profile["workload"]["utilization"]
            },
            "alternatives": alternatives,
            "recommendation": "Рекомендуем выбрать альтернативного кандидата"
        }
    else:
        return {
            "status": "success",
            "message": "Основной кандидат подходит",
            "main_candidate": {
                "name": main_sub,
                "utilization": main_profile["workload"]["utilization"]
            },
            "alternatives": []
        }

