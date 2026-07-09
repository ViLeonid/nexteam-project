from app import app
from extensions import db
from models import ActiveFocusSession
from datetime import datetime
with app.app_context():
    try:
        # Удаляем только таблицу todo
        ActiveFocusSession.__table__.drop(db.engine)
        print("Таблица ActiveFocusSession успешно удалена!")
    except Exception as e:
        print(f"Ошибка при удалении таблицы: {e}")
