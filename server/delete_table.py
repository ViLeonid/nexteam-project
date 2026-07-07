from app import app
from extensions import db
from models import Topic

with app.app_context():
    try:
        # Удаляем только таблицу todo
        Topic.__table__.drop(db.engine)
        print("Таблица FocusSession успешно удалена!")
    except Exception as e:
        print(f"Ошибка при удалении таблицы: {e}")
