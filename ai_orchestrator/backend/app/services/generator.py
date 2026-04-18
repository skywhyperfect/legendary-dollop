import random
import re
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
    
    # Профильные классы
    if grade >= 10:
        if letter in ["А", "В"]: # ФизМат
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

def generate_weekly_schedule(classes: list = None) -> list:
    """Генератор по строгому РУП с делением на группы"""
    if not classes:
        classes = DEFAULT_CLASSES
        
    staff = load_staff()
    if not staff: return []

    subjects_available = list(set([t.get("Предмет") for t in staff if t.get("Предмет") and str(t.get("Предмет")).strip() != "nan"]))
    if not subjects_available:
        subjects_available = ["Математика", "Физика", "Химия", "Биология", "История", "Информатика"]

    teacher_rooms = {}
    room_counter = 101
    for teacher in staff:
        name = str(teacher.get("ФИО", "Unknown")).strip()
        if name not in teacher_rooms:
            teacher_rooms[name] = f"Каб {room_counter}"
            room_counter += 1

    # Запас часов для каждого класса
    class_hours = {c: get_curriculum(c) for c in classes}
    
    schedule = []

    for day in DAYS:
        for lesson_num in LESSONS:
            busy_teachers = set()
            
            for class_name in classes:
                # Фильтруем предметы, по которым еще остались часы у этого класса
                needed = {k: v for k, v in class_hours[class_name].items() if v > 0}
                if not needed:
                    continue # часы кончились
                    
                subject_picked = None
                teacher_found = None
                teacher_name = "Нет свободного учителя"
                room = "Без кабинета"
                is_split = False
                split_teachers = []
                
                # Попытки найти предмет со свободными учителями
                attempts = 0
                while attempts < 20:
                    subj = random.choice(list(needed.keys()))
                    if subj not in subjects_available:
                        # Если предмета вообще нет в школе (например факультатив) - пропустим поиск препода
                        subject_picked = subj
                        teacher_name = "Самопознание / Открытый урок"
                        break
                        
                    # Логика Элективов (Физика или Химия, и т.д.)
                    if subj in ELECTIVE_PAIRS:
                        sub_subjects = ELECTIVE_PAIRS[subj]
                        # Ищем учителя для каждого под-предмета
                        found_both = True
                        current_elective_teachers = []
                        for s_subj in sub_subjects:
                            t_list = [t for t in staff if t.get("Предмет") == s_subj and str(t.get("ФИО")).strip() not in busy_teachers]
                            if t_list:
                                current_elective_teachers.append((s_subj, random.choice(t_list)))
                            else:
                                found_both = False
                                break
                        
                        if found_both:
                            subject_picked = subj
                            is_split = True
                            # Формируем список для записи
                            split_teachers = current_elective_teachers # List of (subject, teacher_dict)
                            break

                    # Логика деления на 2 группы (Английский, Казахский)
                    elif subj in ["Английский язык", "Казахский язык"]:
                        possible_t = [t for t in staff if t.get("Предмет") == subj and str(t.get("ФИО")).strip() not in busy_teachers]
                        if len(possible_t) >= 2:
                            subject_picked = subj
                            is_split = True
                            # Берем 2х разных учителей по ОДНОМУ предмету
                            ts = random.sample(possible_t, 2)
                            split_teachers = [(subj, ts[0]), (subj, ts[1])]
                            break
                    else:
                        # Обычный предмет
                        possible_t = [t for t in staff if t.get("Предмет") == subj and str(t.get("ФИО")).strip() not in busy_teachers]
                        if possible_t:
                            teacher_found = random.choice(possible_t)
                            subject_picked = subj
                            break
                    
                    attempts += 1
                
                # Запись результата
                if subject_picked:
                    class_hours[class_name][subject_picked] -= 1
                    
                    if is_split:
                        # split_teachers это список кортежей (Предмет, ДанныеУчителя)
                        res_lines = []
                        for i, (part_subj, t_data) in enumerate(split_teachers):
                            name = str(t_data.get("ФИО", "")).strip()
                            busy_teachers.add(name)
                            r_num = teacher_rooms.get(name, "???")
                            # Если предметы разные (электив), пишем названия предметов
                            if len(set(p[0] for p in split_teachers)) > 1:
                                res_lines.append(f"[Гр{i+1}] {part_subj}: {name} ({r_num})")
                            else:
                                res_lines.append(f"[Гр{i+1}] {name} ({r_num})")
                        
                        teacher_name = "\n".join(res_lines)
                        room = "Сплит-формат (Split)"
                    elif teacher_found:
                        teacher_name = str(teacher_found.get("ФИО")).strip()
                        busy_teachers.add(teacher_name)
                        room = teacher_rooms.get(teacher_name, "Кабинет X")
                        
                schedule.append({
                    "День": day,
                    "Класс": class_name,
                    "Урок": lesson_num,
                    "Учитель": teacher_name,
                    "Предмет": subject_picked if subject_picked else "Окно",
                    "Кабинет": room,
                    "isSplit": is_split
                })

    def schedule_sort_key(item):
        digits = re.findall(r'\d+', str(item["Класс"]))
        class_num = int(digits[0]) if digits else 0
        letter = "".join(re.findall(r'[А-Яа-яA-Za-z]', str(item["Класс"])))
        day_idx = DAYS.index(item["День"]) if item["День"] in DAYS else 99
        return (class_num, letter, day_idx, item["Урок"])

    schedule.sort(key=schedule_sort_key)
    return schedule
