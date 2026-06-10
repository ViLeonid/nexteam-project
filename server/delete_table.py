from app import app, db, Event

with app.app_context():
    Event.__table__.drop(db.engine)
    print("Таблица Olimpiads удалена")