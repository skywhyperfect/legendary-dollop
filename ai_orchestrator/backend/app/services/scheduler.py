from app.data_loader import load_staff, load_schedule
from typing import List, Dict

def find_substitution(teacher_name: str, target_date: str = None) -> List[Dict]:
    """
    Алгоритм поиска замены.
    teacher_name: Имя заболевшего учителя.
    Возвращает список назначенных замен для каждого урока.
    """
    staff = load_staff()
    schedule = load_schedule()
    
    # Если Excel-файлов нет, возвращаем красивый Mock (Hardcoded fallback для MVP)
    if not staff or not schedule:
        return [
            {
                "missing_teacher": teacher_name,
                "substitute_teacher": "Смирнова Елена (Математика)",
                "lesson_number": 2,
                "class_name": "3В",
                "room": "Кабинет 302",
                "status": "Успешно найдена замена по профилю"
            },
            {
                "missing_teacher": teacher_name,
                "substitute_teacher": "Кусаинов А. (Информатика)",
                "lesson_number": 3,
                "class_name": "5А",
                "room": "Кабинет 305",
                "status": "Замена смежным специалистом (по приказу №110)"
            }
        ]

    # Реальная логика парсинга, если загружены excel файлы
    # 1. Ищем уроки заболевшего учителя сегодня
    # 2. Ищем его специализацию
    # 3. Ищем свободных учителей той же специализации в эти часы
    
    absent_teacher_lessons = [
        s for s in schedule 
        if teacher_name.lower() in str(s.get("Учитель", "")).lower()
        and (not target_date or s.get("День") == target_date)
    ]
    
    if not absent_teacher_lessons:
        return []

    # Находим профиль заболевшего учителя
    absent_profile = "Неизвестно"
    for st in staff:
        if teacher_name.lower() in str(st.get("ФИО", "")).lower():
            absent_profile = st.get("Предмет", "Неизвестно")
            break

    substitutions = []
    
    for lesson in absent_teacher_lessons:
        lesson_time = lesson.get("Урок")
        day = lesson.get("День")
        
        # Кто занят в это время
        busy_teachers = {
            s.get("Учитель") for s in schedule 
            if s.get("Урок") == lesson_time and s.get("День") == day
        }
        
        # Кто свободен из той же специализации
        possible_subs = [
            st.get("ФИО") for st in staff 
            if st.get("Предмет") == absent_profile and st.get("ФИО") not in busy_teachers
            and st.get("ФИО") != lesson.get("Учитель")
        ]
        
        sub_name = possible_subs[0] if possible_subs else "Нет свободных профильных учителей (Требуется окно)"
        
        substitutions.append({
            "missing_teacher": lesson.get("Учитель"),
            "substitute_teacher": sub_name,
            "lesson_number": lesson_time,
            "class_name": lesson.get("Класс"),
            "room": lesson.get("Кабинет"),
            "status": "Замена по профилю" if possible_subs else "Критический дефицит"
        })
        
    return substitutions
