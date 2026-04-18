import random
import re
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from app.data_loader import load_staff

DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
LESSONS = [1, 2, 3, 4, 5, 6]
DEFAULT_CLASSES = [
    "1А", "1Б", "2А", "3Б", "5А", "5Б", "9А", "9Б",
    "10А", "10Б", "11А", "11Б"
]

ELECTIVE_PAIRS = {
    "Электив (Физика/Химия)": ["Физика", "Химия"],
    "Электив (Информатика/Биология)": ["Информатика", "Биология"]
}

# Новая логика Лент (Ribbon)
LENTA_SUBJECTS = ["Английский язык", "Казахский язык"]

def get_curriculum(class_name: str) -> dict:
    digits = re.findall(r'\d+', class_name)
    grade = int(digits[0]) if digits else 0
    letter = "".join(re.findall(r'[А-Яа-яA-Za-z]', class_name)).upper()
    
    # Базовые часы для 1-9 классов
    c = {
        "Математика": 5, "Английский язык": 3, "Казахский язык": 3,
        "Русский язык": 3, "Литература": 2, "Познание мира": 2,
        "Физическая культура": 3, "Музыка": 1, "Изобразительное искусство": 1,
        "Естествознание": 2, "История": 2, "Информатика": 1, 
        "Труд": 1, "Классный час": 1
    }
    
    # Профильные и предпрофильные (9+) классы
    if grade >= 9:
        if grade == 9:
            # Для 9 класса добавляем элективы по выбору (лента)
            c.update({
                "Электив (Физика/Химия)": 2, 
                "Электив (Информатика/Биология)": 2,
                "Физика": 2, "Химия": 2, "Биология": 2, "Информатика": 1
            })
        elif letter in ["А", "В"]: # ФизМат
            c.update({
                "Математика": 10, "Физика": 4, "Информатика": 2, 
                "Электив (Физика/Химия)": 1, "Электив (Информатика/Биология)": 1,
                "Английский язык": 3, "Казахский язык": 3, "История": 2,
                "Биология": 0, "Химия": 0, "Физическая культура": 2
            })
        else: # ХимБио (Б, Г)
            c.update({
                "Математика": 7, "Химия": 4, "Биология": 4,
                "Электив (Физика/Химия)": 1, "Электив (Информатика/Биология)": 1,
                "Английский язык": 3, "Казахский язык": 3, "История": 2,
                "Физика": 0, "Информатика": 0, "Физическая культура": 3
            })
            
    # Добиваем до 30 часов
    total = sum(c.values())
    if total < 30:
        c["Факультатив"] = 30 - total
    return c

ROOM_TYPE_MAP = {
    "Физическая культура": ["спортзал", "зал"],
    "Химия": ["химия", "лаборатория"],
    "Биология": ["биология", "лаборатория"],
    "Информатика": ["компьютерный", "информатика"],
    "Музыка": ["музыкальный", "музыка"],
    "Английский язык": ["лингвафонный", "лингвафон", "общий"],
    "Казахский язык": ["общий"],
    "Русский язык": ["общий"],
    "Литература": ["общий"],
}

DEFAULT_ROOM_INVENTORY = [
    {"name": "Кабинет 101", "capacity": 30, "types": ["общий"]},
    {"name": "Кабинет 102", "capacity": 30, "types": ["общий"]},
    {"name": "Кабинет 201", "capacity": 30, "types": ["общий"]},
    {"name": "Кабинет 202", "capacity": 30, "types": ["общий"]},
    {"name": "Компьютерный класс", "capacity": 24, "types": ["компьютерный", "информатика"]},
    {"name": "Лаборатория химии", "capacity": 18, "types": ["химия", "лаборатория"]},
    {"name": "Лаборатория биологии", "capacity": 18, "types": ["биология", "лаборатория"]},
    {"name": "Спортзал", "capacity": 40, "types": ["спортзал", "зал"]},
    {"name": "Музыкальный кабинет", "capacity": 22, "types": ["музыкальный"]},
    {"name": "Лингвафонный кабинет", "capacity": 16, "types": ["лингвафонный", "лингвафон"]},
]


def parse_unavailable_slots(raw: Any) -> Set[tuple[str, int]]:
    slots: Set[tuple[str, int]] = set()
    if not raw:
        return slots
    if isinstance(raw, str):
        raw = [raw]
    for item in raw:
        if isinstance(item, dict):
            day = item.get("day") or item.get("День") or item.get("day_name")
            lesson = item.get("lesson") or item.get("урок") or item.get("lesson_number")
        else:
            continue
        try:
            if day and lesson:
                slots.add((str(day), int(lesson)))
        except Exception:
            continue
    return slots


def merge_class_load(default_load: Dict[str, int], override: Dict[str, Any]) -> Dict[str, int]:
    result = default_load.copy()
    for subject, hours in (override or {}).items():
        try:
            result[str(subject)] = int(hours)
        except Exception:
            continue
    return result


def build_teacher_profiles(staff: list, constraints: Optional[list] = None) -> Dict[str, Dict[str, Any]]:
    profiles: Dict[str, Dict[str, Any]] = {}
    for teacher in staff:
        name = str(teacher.get("ФИО", "")).strip()
        if not name:
            continue
        subjects = []
        if teacher.get("Предмет"):
            subjects.append(str(teacher.get("Предмет")))
        max_hours = 20
        if teacher.get("Ставка"):
            try:
                max_hours = int(teacher.get("Ставка"))
            except Exception:
                pass
        unavailable = parse_unavailable_slots(teacher.get("Ограничения"))
        profiles[name] = {
            "name": name,
            "subjects": subjects,
            "max_hours": max_hours,
            "unavailable": unavailable,
            "assigned_hours": 0,
        }

    for override in (constraints or []):
        name = str(override.get("teacher_name") or override.get("ФИО") or override.get("name", "")).strip()
        if not name:
            continue
        profile = profiles.setdefault(name, {
            "name": name,
            "subjects": [],
            "max_hours": 20,
            "unavailable": set(),
            "assigned_hours": 0,
        })
        if override.get("max_hours") is not None:
            try:
                profile["max_hours"] = int(override["max_hours"])
            except Exception:
                pass
        if override.get("subjects"):
            profile["subjects"] = [str(s) for s in override.get("subjects") if s]
        if override.get("unavailable"):
            profile["unavailable"] = profile["unavailable"].union(parse_unavailable_slots(override.get("unavailable")))
    return profiles


def build_room_inventory(overrides: Optional[list] = None) -> list:
    rooms = {room["name"]: {**room, "unavailable": set()} for room in DEFAULT_ROOM_INVENTORY}
    for override in (overrides or []):
        name = str(override.get("room_name") or override.get("name", "")).strip()
        if not name:
            continue
        room = rooms.setdefault(name, {
            "name": name,
            "capacity": int(override.get("capacity", 0)) if override.get("capacity") else 0,
            "types": [str(t) for t in override.get("types", []) if t],
            "unavailable": set()
        })
        if override.get("capacity") is not None:
            try:
                room["capacity"] = int(override["capacity"])
            except Exception:
                pass
        if override.get("types"):
            room["types"] = [str(t) for t in override.get("types") if t]
        if override.get("unavailable"):
            room["unavailable"] = room["unavailable"].union(parse_unavailable_slots(override.get("unavailable")))
    return list(rooms.values())


def is_teacher_available(profile: Dict[str, Any], day: str, lesson: int, busy_teachers: Set[str]) -> bool:
    return (
        profile["name"] not in busy_teachers and
        (day, lesson) not in profile["unavailable"] and
        profile["assigned_hours"] < profile["max_hours"]
    )


def choose_teacher(subject: str, teachers: Dict[str, Dict[str, Any]], day: str, lesson: int, busy_teachers: Set[str], exclude: Optional[Set[str]] = None) -> Optional[Dict[str, Any]]:
    ordered = []
    for profile in teachers.values():
        if exclude and profile["name"] in exclude:
            continue
        if not is_teacher_available(profile, day, lesson, busy_teachers):
            continue
        score = 2 if subject in profile["subjects"] else 1
        ordered.append((score, profile))
    ordered.sort(key=lambda item: (-item[0], item[1]["assigned_hours"]))
    if ordered:
        return ordered[0][1]
    return None


def choose_room(subject: str, rooms: list, day: str, lesson: int, busy_rooms: Set[str]) -> Optional[Dict[str, Any]]:
    desired = ROOM_TYPE_MAP.get(subject, ["общий"])
    candidates = [room for room in rooms if room["name"] not in busy_rooms and (day, lesson) not in room["unavailable"] and any(rt in room.get("types", []) for rt in desired)]
    if not candidates:
        candidates = [room for room in rooms if room["name"] not in busy_rooms and (day, lesson) not in room["unavailable"]]
    return random.choice(candidates) if candidates else None


def merge_constraints(class_names: list, constraints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "class_load": {item.get("class_name"): item.get("subject_hours") for item in (constraints or {}).get("class_load", []) if item.get("class_name")},
        "teacher_constraints": (constraints or {}).get("teacher_constraints", []),
        "room_constraints": (constraints or {}).get("room_constraints", []),
    }


def get_db_tasks():
    """Получает задачи из БД для привязки к персоналу."""
    tasks = []
    try:
        conn = sqlite3.connect("orchestrator.db")
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM task_reminders WHERE is_completed=0").fetchall()
        tasks = [dict(r) for r in rows]
        conn.close()
    except:
        pass
    return tasks

def generate_weekly_schedule(classes: list = None, constraints: Optional[Dict[str, Any]] = None) -> list:
    """Генератор по строгому РУП с логикой Лент и деления на группы."""
    if not classes:
        classes = DEFAULT_CLASSES
        
    staff = load_staff()
    if not staff: return []

    merged = merge_constraints(classes, constraints)
    teacher_profiles = build_teacher_profiles(staff, merged["teacher_constraints"])
    room_inventory = build_room_inventory(merged["room_constraints"])

    subjects_available = list(set([t.get("Предмет") for t in staff if t.get("Предмет") and str(t.get("Предмет")).strip() != "nan"]))
    if not subjects_available:
        subjects_available = ["Математика", "Физика", "Химия", "Биология", "История", "Информатика"]

    class_hours = {
        c: merge_class_load(get_curriculum(c), merged["class_load"].get(c, {}))
        for c in classes
    }
    schedule = []

    # Группируем классы по параллелям для Лент
    grades = {}
    for c in classes:
        g = re.findall(r'\d+', c)[0]
        if g not in grades: grades[g] = []
        grades[g].append(c)

    for day in DAYS:
        for lesson_num in LESSONS:
            busy_teachers = set()
            busy_rooms = set()
            lenta_locked_classes = set()

            # 1. Попытка поставить Ленту (Ribbon) для параллелей
            for grade_str, parallel_classes in grades.items():
                if len(parallel_classes) < 2: continue
                grade_int = int(grade_str)
                
                # Список кандидатов на ленту (Языки для всех, Профильные для 9+)
                potential_lentas = list(LENTA_SUBJECTS)
                if grade_int >= 9:
                    potential_lentas.extend(list(ELECTIVE_PAIRS.keys()))
                
                lenta_subj = random.choice(potential_lentas)
                
                # Проверяем, нужны ли часы по этому предмету ВСЕМ классам в параллели
                can_do_lenta = True
                for pc in parallel_classes:
                    if class_hours[pc].get(lenta_subj, 0) == 0:
                        can_do_lenta = False
                        break
                
                if can_do_lenta:
                    if lenta_subj in LENTA_SUBJECTS:
                        selected_teachers = []
                        for _ in range(4):
                            teacher_profile = choose_teacher(lenta_subj, teacher_profiles, day, lesson_num, busy_teachers, exclude={t["name"] for t in selected_teachers})
                            if teacher_profile:
                                selected_teachers.append(teacher_profile)
                        if len(selected_teachers) == 4:
                            for pc in parallel_classes:
                                class_hours[pc][lenta_subj] -= 1
                                lenta_locked_classes.add(pc)
                                res_lines = [f"[Уровень {i+1}] {t['name']}" for i, t in enumerate(selected_teachers)]
                                schedule.append({
                                    "День": day, "Класс": pc, "Урок": lesson_num,
                                    "Учитель": "\n".join(res_lines), "Предмет": f"ЛЕНТА: {lenta_subj}",
                                    "Кабинет": "Параллель (Ribbon)", "isSplit": True, "type": "lenta"
                                })
                            for t in selected_teachers:
                                busy_teachers.add(t["name"])
                                t["assigned_hours"] += 1
                    elif lenta_subj in ELECTIVE_PAIRS:
                        sub_subjects = ELECTIVE_PAIRS[lenta_subj]
                        selected_for_ribbon = []
                        for sub_s in sub_subjects:
                            chosen = choose_teacher(sub_s, teacher_profiles, day, lesson_num, busy_teachers)
                            if chosen:
                                selected_for_ribbon.append((sub_s, chosen))
                            else:
                                selected_for_ribbon = []
                                break
                        if selected_for_ribbon:
                            for pc in parallel_classes:
                                class_hours[pc][lenta_subj] -= 1
                                lenta_locked_classes.add(pc)
                                res_lines = [f"[{sub_s}] {t['name']}" for sub_s, t in selected_for_ribbon]
                                schedule.append({
                                    "День": day, "Класс": pc, "Урок": lesson_num,
                                    "Учитель": "\n".join(res_lines), "Предмет": f"ЛЕНТА: {lenta_subj}",
                                    "Кабинет": "Параллель (Ribbon)", "isSplit": True, "type": "lenta"
                                })
                            for _, t in selected_for_ribbon:
                                busy_teachers.add(t["name"])
                                t["assigned_hours"] += 1

            # 2. Обычные уроки для остальных классов
            for class_name in classes:
                if class_name in lenta_locked_classes: continue
                
                needed = {k: v for k, v in class_hours[class_name].items() if v > 0}
                if not needed: continue
                    
                subject_picked = None
                teacher_name = "Нет свободного учителя"
                room = "Без кабинета"
                is_split = False
                split_teachers = []
                teacher_found = None
                
                attempts = 0
                while attempts < 20:
                    subj = random.choice(list(needed.keys()))
                    if subj not in subjects_available:
                        subject_picked = subj
                        teacher_name = "Самопознание / Открытый урок"
                        break
                        
                    if subj in ELECTIVE_PAIRS:
                        sub_subjects = ELECTIVE_PAIRS[subj]
                        selected = []
                        for s_subj in sub_subjects:
                            teacher_profile = choose_teacher(s_subj, teacher_profiles, day, lesson_num, busy_teachers)
                            if teacher_profile:
                                selected.append((s_subj, teacher_profile))
                            else:
                                selected = []
                                break
                        if selected:
                            subject_picked = subj
                            is_split = True
                            split_teachers = selected
                            break

                    elif subj in ["Английский язык", "Казахский язык"]:
                        first = choose_teacher(subj, teacher_profiles, day, lesson_num, busy_teachers)
                        second = None
                        if first:
                            second = choose_teacher(subj, teacher_profiles, day, lesson_num, busy_teachers, exclude={first["name"]})
                        if first and second:
                            subject_picked = subj
                            is_split = True
                            split_teachers = [(subj, first), (subj, second)]
                            break
                    else:
                        teacher_profile = choose_teacher(subj, teacher_profiles, day, lesson_num, busy_teachers)
                        if teacher_profile:
                            teacher_found = teacher_profile
                            subject_picked = subj
                            break
                    attempts += 1
                
                if subject_picked:
                    class_hours[class_name][subject_picked] -= 1
                    if is_split:
                        res_lines = []
                        for i, (part_subj, t_profile) in enumerate(split_teachers):
                            name = t_profile["name"]
                            busy_teachers.add(name)
                            t_profile["assigned_hours"] += 1
                            res_lines.append(f"[Гр{i+1}] {part_subj}: {name}")
                        teacher_name = "\n".join(res_lines)
                        room = "Сплит-формат (Split)"
                    elif teacher_found:
                        teacher_name = teacher_found["name"]
                        busy_teachers.add(teacher_name)
                        teacher_found["assigned_hours"] += 1
                        room_choice = choose_room(subject_picked, room_inventory, day, lesson_num, busy_rooms)
                        if room_choice:
                            room = room_choice["name"]
                            busy_rooms.add(room)
                        else:
                            room = "Кабинет не найден"
                        
                schedule.append({
                    "День": day, "Класс": class_name, "Урок": lesson_num,
                    "Учитель": teacher_name, "Предмет": subject_picked if subject_picked else "Окно",
                    "Кабинет": room, "isSplit": is_split, "type": "regular"
                })

    def schedule_sort_key(item):
        digits = re.findall(r'\d+', str(item["Класс"]))
        class_num = int(digits[0]) if digits else 0
        letter = "".join(re.findall(r'[А-Яа-яA-Za-z]', str(item["Класс"])))
        day_idx = DAYS.index(item["День"]) if item["День"] in DAYS else 99
        return (class_num, letter, day_idx, item["Урок"])

    schedule.sort(key=schedule_sort_key)
    return schedule

def generate_staff_schedule() -> list:
    """Генерация персонализированного расписания для Admin и Техперсонала."""
    staff = load_staff()
    db_tasks = get_db_tasks()
    
    staff_schedule = []
    # Категории персонала
    roles = {
        "Директор": ["Сарсенбаев А.Т."],
        "Завхоз": ["Ахмет (Завхоз)"],
        "Охрана": ["Охрана Aqbobek"],
        "Айгерим": ["Айгерим (Ивент-менеджер)"]
    }

    for day in DAYS:
        for lesson_num in LESSONS:
            for role_name, members in roles.items():
                for member in members:
                    # Подбираем задачу из БД, если она подходит по смыслу
                    task_for_today = None
                    for t in db_tasks:
                        if role_name.lower() in t["assignee"].lower() or member.lower() in t["assignee"].lower():
                            # Если задача еще не поставлена в этот день
                            task_for_today = t
                            db_tasks.remove(t)
                            break
                    
                    if task_for_today:
                        activity = task_for_today["title"]
                        room = task_for_today.get("location", "Школа")
                        type_label = "task"
                    else:
                        # Плановые дела
                        if role_name == "Директор":
                            activity = "Прием родителей / Контроль уроков"
                            room = "Кабинет директора"
                        elif role_name == "Завхоз":
                            activity = "Плановый обход территории"
                            room = "Вся школа"
                        else:
                            activity = "Дежурство / Мониторинг"
                            room = "Пост №1"
                        type_label = "routine"
                    
                    staff_schedule.append({
                        "День": day, "Сотрудник": member, "Роль": role_name,
                        "Урок": lesson_num, "Активность": activity,
                        "Место": room, "type": type_label
                    })
    return staff_schedule
