from app import app
from extensions import db
from models import FocusSession

with app.app_context():
    try:
        # Удаляем только таблицу todo
        FocusSession.__table__.drop(db.engine)
        print("Таблица Olympiads успешно удалена!")
    except Exception as e:
        print(f"Ошибка при удалении таблицы: {e}")
