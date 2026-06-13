from app import app
from extensions import db
from models import Olympiads

with app.app_context():
    try:
        # Удаляем только таблицу todo
        Olympiads.__table__.drop(db.engine)
        print("Таблица Olympiads успешно удалена!")
    except Exception as e:
        print(f"Ошибка при удалении таблицы: {e}")
