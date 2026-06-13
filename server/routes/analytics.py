from flask import Blueprint, jsonify, request, session
from datetime import datetime

from models import Event

analytics_bp = Blueprint(
    "analytics",
    __name__
)


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
        "blue": {"label": "Обычные дела", "hex": "#00f0ff"},     # Электрический циан
        "red": {"label": "Дедлайны / Задачи", "hex": "#ff007f"},  # Неоновый розовый
        "purple": {"label": "Задачи от ИИ", "hex": "#a020f0"}    # Неоновый фиолетовый
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