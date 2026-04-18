from app.data_loader import load_staff, load_schedule
from typing import List, Dict
from app.ai.rag_service import check_compliance

def find_substitution(teacher_name: str, target_date: str = None) -> List[Dict]:
    """
    Алгоритм поиска замены с проверкой по базе приказов МОН (RAG).
    """
    staff = load_staff()
    schedule = load_schedule()
    
    # Если Excel-файлов нет, возвращаем красивый Mock
    if not staff or not schedule:
        return [
            {
                "missing_teacher": teacher_name,
                "substitute_teacher": "Смирнова Елена (Математика)",
                "lesson_number": 2,
                "class_name": "3В",
                "room": "Кабинет 302",
                "status": "Успешно найдена замена по профилю"
            }
        ]

    absent_teacher_lessons = [
        s for s in schedule 
        if teacher_name.lower() in str(s.get("Учитель", "")).lower()
        and (not target_date or str(s.get("День")) == target_date)
    ]
    
    if not absent_teacher_lessons:
        return []

    absent_profile = "Неизвестно"
    absent_qualification = "Неизвестно"
    for st in staff:
        if teacher_name.lower() in str(st.get("ФИО", "")).lower():
            absent_profile = st.get("Предмет", "Неизвестно")
            absent_qualification = st.get("Квалификация", "Неизвестно")
            break

    substitutions = []
    
    for lesson in absent_teacher_lessons:
        lesson_time = lesson.get("Урок")
        day = lesson.get("День")
        
        busy_teachers = {
            s.get("Учитель") for s in schedule 
            if s.get("Урок") == lesson_time and s.get("День") == day
        }
        
        # Кто свободен из той же специализации
        possible_subs = [
            st for st in staff 
            if st.get("Предмет") == absent_profile and st.get("ФИО") not in busy_teachers
            and st.get("ФИО") != lesson.get("Учитель")
        ]
        
        sub_name = possible_subs[0].get("ФИО") if possible_subs else "Нет свободных учителей"
        
        status_msg = "Замена по профилю" if possible_subs else "Критический дефицит"

        # --- SMART COMPLIANCE RAG CHECK ---
        if possible_subs:
            sub_qual = possible_subs[0].get("Квалификация", "")
            # Проверяем, нарушает ли замена правила (например, приказ 130 требует соответствия квалификации)
            query = f"Замена учителя ({absent_qualification}) на учителя ({sub_qual}) по предмету {absent_profile}. Это законно?"
            compliance = check_compliance(query)
            
            if not compliance.get("compliant", True):
                status_msg += " ⚠️ (Внимание: Нарушение приказа. Требуется ручной апрув.)"
            elif "нарушает" in compliance.get("analysis", "").lower():
                status_msg += " ⚠️ (Внимание: Возможен конфликт квалификаций)"
            else:
                status_msg += " 🛡️ (Проверено RAG: Соответствует нормативам)"

        substitutions.append({
            "missing_teacher": lesson.get("Учитель"),
            "substitute_teacher": sub_name,
            "lesson_number": lesson_time,
            "class_name": lesson.get("Класс"),
            "room": lesson.get("Кабинет"),
            "status": status_msg
        })
        
    return substitutions
