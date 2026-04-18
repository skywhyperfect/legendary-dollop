import sqlite3
import os

def setup():
    # Ищем все возможные БД и чистим их надежно
    db_paths = [
        'ai_orchestrator/backend/orchestrator.db',
        'ai_orchestrator/orchestrator.db',
        'orchestrator.db',
        'ai_orchestrator/backend/school_bot.db'
    ]
    
    found_db = None
    for p in db_paths:
        if os.path.exists(p):
            found_db = p
            print(f"🔄 Подключение к базе: {p}")
            conn = sqlite3.connect(p)
            cur = conn.cursor()
            
            # --- 1. ОЧИСТКА СООБЩЕНИЙ (Telegram/WA) ---
            try:
                cur.execute("DELETE FROM tg_messages")
                print("✅ Таблица сообщений (tg_messages) очищена.")
            except Exception as e:
                pass
                
            try:
                cur.execute("DELETE FROM bot_messages")
            except:
                pass

            # --- 2. ДОБАВЛЕНИЕ 8 КРАСИВЫХ ЗАДАЧ ---
            try:
                # Очищаем старые задачи
                cur.execute("DELETE FROM task_reminders")
                
                tasks = [
                    # В работе (5)
                    ("Починить трубу в фойе школы", "Ахмет (Завхоз)", "Сегодня", 0, 0),
                    ("Подготовить актовый зал к AIS Hack 3.0", "Айгерим", "До среды", 0, 0),
                    ("Заказать 20 бутылей воды для младших классов", "Назкен", "Завтра", 0, 0),
                    ("Проанализировать посещаемость за неделю", "Секретарь", "Пятница", 0, 0),
                    ("Организовать замену для заболевшего историка", "Директор", "Срочно", 0, 0),
                    # Выполненные (3)
                    ("Снять показания тепловых счетчиков", "Ахмет (Завхоз)", "Среда", 0, 1),
                    ("Разослать письмо родителям 3В класса", "Смирнова Е.", "Сегодня", 0, 1),
                    ("Составить меню столовой на неделю", "Шеф-повар", "Пятница", 0, 1)
                ]
                
                cur.executemany("INSERT INTO task_reminders (title, assignee, deadline, is_accepted, is_completed) VALUES (?, ?, ?, ?, ?)", tasks)
                print("✅ 8 идеальных задач для демо успешно загружены!")
            except Exception as e:
                print(f"❌ Ошибка с таблицей задач: {e}")
                
            conn.commit()
            conn.close()

if __name__ == "__main__":
    setup()
