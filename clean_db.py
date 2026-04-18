import sqlite3
import os

def clean():
    # Ищем БД в возможных местах
    paths = ['ai_orchestrator/backend/orchestrator.db', 'ai_orchestrator/orchestrator.db', 'orchestrator.db']
    db_path = None
    
    for p in paths:
        if os.path.exists(p):
            db_path = p
            break
            
    if not db_path:
        print("❌ Ошибка: база данных orchestrator.db не найдена. Убедитесь, что бэкенд был запущен хотя бы один раз.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Удаляем историю сообщений
        cursor.execute("DELETE FROM tg_messages;")
        
        conn.commit()
        conn.close()
        print(f"✅ База ({db_path}) очищена! Лента сообщений снова пуста.")
    except Exception as e:
        print(f"❌ Ошибка очистки: {e}")

if __name__ == "__main__":
    clean()
