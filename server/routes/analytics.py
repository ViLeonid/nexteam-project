from flask import Blueprint, jsonify, request, session
from datetime import datetime
from extensions import db
from models import Event, FocusSession
from sqlalchemy import func

analytics_bp = Blueprint(
    "analytics",
    __name__
)
from datetime import datetime, timedelta
@analytics_bp.route('/api/analytics/hours-of-subject')
def hours_of_subject():
    current_user_id = session.get('user_id')

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    event_class = "blue"
    labels = []
    values = []
    for i in range(9, -1, -1):
        day = datetime.now().date() - timedelta(days=i)

        events = Event.query.filter(
            Event.user_id == current_user_id,
            db.func.date(Event.start_time) == day,
            Event.color == event_class
        ).all()

        hours = 0

        for event in events:
            duration = event.end_time - event.start_time
            hours += duration.total_seconds() / 3600

        labels.append(day.strftime('%d.%m'))
        values.append(round(hours, 1))

    return jsonify({
        "labels": labels,
        "values": values
    })

@analytics_bp.route('/api/analytics/tasks-last-10-days')
def tasks_last_10_days():
    current_user_id = session.get('user_id')

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    labels = []
    values = []

    for i in range(9, -1, -1):
        day = datetime.now().date() - timedelta(days=i)

        events = Event.query.filter(
            Event.user_id == current_user_id,
            db.func.date(Event.start_time) == day
        ).all()

        hours = 0

        for event in events:
            duration = event.end_time - event.start_time
            hours += duration.total_seconds() / 3600

        labels.append(day.strftime('%d.%m'))
        values.append(round(hours, 1))

    return jsonify({
        "labels": labels,
        "values": values
    })

@analytics_bp.route('/api/analytics/today', methods=['GET'])
def get_today_analytics():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    # 1. Определяем границы текущего дня (от 00:00:00 до 23:59:59)
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
    today_end = datetime(now.year, now.month, now.day, 23, 59, 59)

    # 2. Берем события пользователя, которые начинаются СЕГОДНЯ
    events = Event.query.filter(
        Event.user_id == current_user_id,
        Event.start_time >= today_start,
        Event.start_time <= today_end
    ).all()

    if not events:
        return jsonify({
            "labels": ["Свободный день"],
            "values": [24],
            "colors": ["#1f293d"]  # Темный пустой сектор вместо серого
        })

    # Карта цветов для категорий
        # Карта неоновых цветов
    color_map = {
    "green": {
        "label": "Спорт",
        "hex": "#22c55e"
    },
    "blue": {
        "label": "Отдых",
        "hex": "#3b82f6"
    },
    "yellow": {
        "label": "Чтение",
        "hex": "#f59e0b"
    },
    "red": {
        "label": "Олфиз",
        "hex": "#ef4444"
    },
    "purple": {
        "label": "Школа",
        "hex": "#8b5cf6"
    },
    "orange": {
        "label": "Еда",
        "hex": "#f97316"
    }
}




    # Словарь для суммирования часов по категориям
    # Пример: { "blue": 2.5, "red": 1.0 }
    duration_stats = {}

    for ev in events:
        color_name = ev.color if ev.color in color_map else "blue"

        # Считаем длительность события в часах
        duration_timedelta = ev.end_time - ev.start_time
        duration_hours = duration_timedelta.total_seconds() / 3600.0

        # Если событие внезапно имеет некорректное время, берем минимум 30 минут
        if duration_hours <= 0:
            duration_hours = 0.5

        duration_stats[color_name] = duration_stats.get(color_name, 0.0) + duration_hours

    # 3. Собираем списки для фронтенда
    labels = []
    values = []
    colors = []

    for color_name, hours in duration_stats.items():
        labels.append(color_map[color_name]["label"])
        # Округляем часы до 1 знака после запятой (например, 1.5 часа)
        values.append(round(hours, 1))
        colors.append(color_map[color_name]["hex"])

    return jsonify({
        "labels": labels,
        "values": values,
        "colors": colors
    })

@analytics_bp.route("/api/analytics/summary", methods=["GET"])
def analytics_summary():
    current_user_id = session.get("user_id")

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    # Все сессии пользователя
    sessions = FocusSession.query.filter_by(user_id=current_user_id).all()

    if not sessions:
        return jsonify({
            "total_hours": 0,
            "week_hours": 0,
            "favorite_subject": "-",
            "favorite_subject_hours": 0,
            "total_tasks": 0,
            "week_tasks": 0,
            "topics_count": 0,
            "last_topic": "-",
            "favorite_topic": "-",
            "favorite_topic_hours": 0,
            "average_session": 0,
            "sessions_count": 0
        })

    now = datetime.now()
    week_ago = now - timedelta(days=7)

    # ---------------- Всего часов ----------------

    total_seconds = sum(fs.real_time for fs in sessions)
    total_hours = round(total_seconds / 3600, 1)

    week_seconds = sum(
        fs.real_time
        for fs in sessions
        if fs.end_time >= week_ago
    )

    week_hours = round(week_seconds / 3600, 1)

    # ---------------- Задачи ----------------

    total_tasks = sum(fs.count_tasks for fs in sessions)

    week_tasks = sum(
        fs.count_tasks
        for fs in sessions
        if fs.end_time >= week_ago
    )

    # ---------------- Любимый предмет ----------------

    subject_stats = (
        db.session.query(
            FocusSession.subject,
            func.sum(FocusSession.real_time)
        )
        .filter(FocusSession.user_id == current_user_id)
        .group_by(FocusSession.subject)
        .order_by(func.sum(FocusSession.real_time).desc())
        .first()
    )

    favorite_subject = "-"
    favorite_subject_hours = 0

    if subject_stats:
        favorite_subject = subject_stats[0]
        favorite_subject_hours = round(subject_stats[1] / 3600, 1)

    # ---------------- Темы ----------------

    topics_count = (
        db.session.query(
            func.count(func.distinct(FocusSession.topic))
        )
        .filter(FocusSession.user_id == current_user_id)
        .scalar()
    )

    last_topic = (
        FocusSession.query
        .filter_by(user_id=current_user_id)
        .order_by(FocusSession.end_time.desc())
        .first()
    )

    last_topic_name = last_topic.topic if last_topic else "-"

    favorite_topic = (
        db.session.query(
            FocusSession.topic,
            func.sum(FocusSession.real_time)
        )
        .filter(FocusSession.user_id == current_user_id)
        .group_by(FocusSession.topic)
        .order_by(func.sum(FocusSession.real_time).desc())
        .first()
    )

    favorite_topic_name = "-"
    favorite_topic_hours = 0

    if favorite_topic:
        favorite_topic_name = favorite_topic[0]
        favorite_topic_hours = round(favorite_topic[1] / 3600, 1)

    # ---------------- Средняя сессия ----------------

    average_session = round(total_seconds / len(sessions) / 60)

    return jsonify({
        "total_hours": total_hours,
        "week_hours": week_hours,

        "favorite_subject": favorite_subject,
        "favorite_subject_hours": favorite_subject_hours,

        "total_tasks": total_tasks,
        "week_tasks": week_tasks,

        "topics_count": topics_count,
        "last_topic": last_topic_name,

        "favorite_topic": favorite_topic_name,
        "favorite_topic_hours": favorite_topic_hours,

        "average_session": average_session,
        "sessions_count": len(sessions)
    })

@analytics_bp.route("/api/analytics/focus-today", methods=["GET"])
def focus_today():
    current_user_id = session.get("user_id")

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    now = datetime.now()

    today_start = datetime(now.year, now.month, now.day)
    tomorrow_start = today_start + timedelta(days=1)

    # Все завершенные Focus-сессии за сегодня
    sessions = (
        FocusSession.query
        .filter(
            FocusSession.user_id == current_user_id,
            FocusSession.end_time >= today_start,
            FocusSession.end_time < tomorrow_start
        )
        .all()
    )

    worked_seconds = sum(fs.real_time for fs in sessions)
    sessions_count = len(sessions)

    goal_seconds = 3 * 60 * 60      # 3 часа

    progress = min(
        round(worked_seconds / goal_seconds * 100),
        100
    )

    return jsonify({
        "worked_seconds": worked_seconds,
        "goal_seconds": goal_seconds,
        "sessions_count": sessions_count,
        "progress": progress
    })