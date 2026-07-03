from flask import Blueprint, jsonify, request, session

from utils import parse_datetime_with_seconds
from models import FocusSession
from extensions import db

focus_bp = Blueprint(
    "focus",
    __name__
)

@focus_bp.route('/api/focus', methods=['GET'])
def focus():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    all_fs = FocusSession.query.filter_by().all()
    output = []
    for fs in all_fs:
            output.append({
                    "id": fs.id,
                    "start_time": fs.start_time,
                    "end_time": fs.end_time,
                    "subject": fs.subject,
                    "real_time": fs.real_time,
                    "is_tasks": fs.is_tasks,
                    "topic": fs.topic,
                    "goal": fs.goal,
                    "count_tasks": fs.count_tasks
                })
    return jsonify({'status': 'success', 'focus_sessions': output})


@focus_bp.route('/api/add_fs', methods=['POST'])
def add_fs():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    fs = request.get_json()
    new_fs = FocusSession(
        start_time=parse_datetime_with_seconds(fs.get("start_time")),
        end_time=parse_datetime_with_seconds(fs.get("end_time")),
        subject=fs.get("subject"),
        real_time=fs.get("real_time"),
        is_tasks=fs.get("is_tasks"),
        topic=fs.get("topic"),
        goal=fs.get("goal"),
        count_tasks=fs.get("count_tasks"),
        user_id=current_user_id
    )
    db.session.add(new_fs)
    db.session.commit()
    return jsonify({"status": "success"})
