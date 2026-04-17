import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_DIR = os.path.join(BASE_DIR, "data", "mock")

def load_staff() -> list:
    """ Загрузка базы сотрудников и нагрузки из Excel """
    file_path = os.path.join(MOCK_DIR, "нагрузка учителей для хакатона 2025-2026.xlsx")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Returning mock data.")
        return []
        
    try:
        df = pd.read_excel(file_path)
        # Пример конвертации датафрейма в список словарей
        # Зависит от структуры файла, пока делаем fallback
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading staff: {e}")
        return []

def load_schedule() -> list:
    """ Загрузка полного расписания на неделю из Excel """
    file_path = os.path.join(MOCK_DIR, "для хакатона расписание.xlsx")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Returning mock data.")
        return []
        
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading schedule: {e}")
        return []
