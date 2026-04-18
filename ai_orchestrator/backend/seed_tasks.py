from app.db.database import SessionLocal, engine
from app.db.models import TaskReminder, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_tasks():
    db = SessionLocal()
    
    # Check if we already have tasks to avoid duplicates
    if db.query(TaskReminder).count() > 0:
        print("Database already has tasks. Skipping seeding.")
        db.close()
        return

    mock_tasks = [
        TaskReminder(
            title="Починить парту в кабинете 12", 
            assignee="Ахмет (Завхоз)", 
            deadline="Сегодня до 14:00", 
            is_completed=False
        ),
        TaskReminder(
            title="Подготовить актовый зал к хакатону", 
            assignee="Айгерим", 
            deadline="До среды", 
            is_completed=False
        ),
        TaskReminder(
            title="Заказать воду для всех классов (20 бутылей)", 
            assignee="Назкен", 
            deadline="Завтра", 
            is_completed=False
        ),
        TaskReminder(
            title="Собрать отчетность по питанию за неделю", 
            assignee="Секретарь Назкен", 
            deadline="Пятница", 
            is_completed=True
        ),
        TaskReminder(
            title="Проверить журналы 5-х классов", 
            assignee="Завуч", 
            deadline="Понедельник", 
            is_completed=False
        )
    ]

    try:
        db.add_all(mock_tasks)
        db.commit()
        print(f"Successfully seeded {len(mock_tasks)} tasks.")
    except Exception as e:
        print(f"Error seeding tasks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_tasks()
