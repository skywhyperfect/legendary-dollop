import sqlite3
import os

DB_PATH = "ai_orchestrator/backend/orchestrator.db"

def reset_db():
    if os.path.exists(DB_PATH):
        print(f"🗑 Удаление старой базы: {DB_PATH}")
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создание таблицы задач (TaskReminder)
    cursor.execute('''
    CREATE TABLE task_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        assignee TEXT NOT NULL,
        deadline TEXT NOT NULL,
        is_accepted BOOLEAN DEFAULT 0,
        is_completed BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Создание таблицы Telegram сообщений (tg_messages)
    cursor.execute('''
    CREATE TABLE tg_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        parsed_type TEXT DEFAULT 'other',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # --- ЗОЛОТЫЕ ПРИМЕРЫ ДЛЯ ДЕМО ---
    demo_tasks = [
        ("Заказать 20 бутылей воды для начальной школы", "Назкен", "Завтра до 10:00", 1, 0),
        ("Подготовить актовый зал к родительскому собранию", "Айгерим", "Среда, 15:00", 1, 1),
        ("Починить проектор в кабинете 302", "Ахмет", "Срочно", 0, 0),
        ("Распечатать расписание на следующую неделю", "Секретарь", "Пятница", 0, 0)
    ]
    
    cursor.executemany(
        "INSERT INTO task_reminders (title, assignee, deadline, is_accepted, is_completed) VALUES (?, ?, ?, ?, ?)",
        demo_tasks
    )
    
    # Примеры сообщений в ленте
    demo_messages = [
        ("1А — Смирнова", "25 детей, 2 болеют.", "food"),
        ("Ахмет (Завхоз)", "В кабинете 12 сломалась парта на последнем ряду.", "incident"),
        ("Аскар (Математика)", "Коллеги, я с температурой 39. Сегодня не смогу прийти.", "absence")
    ]
    
    cursor.executemany(
        "INSERT INTO tg_messages (sender, text, parsed_type) VALUES (?, ?, ?)",
        demo_messages
    )
    
    conn.commit()
    conn.close()
    print("✅ База данных успешно инициализирована чистыми данными для демо!")

if __name__ == "__main__":
    reset_db()
