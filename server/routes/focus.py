from flask import Blueprint, jsonify, request, session

from utils import parse_datetime_with_seconds
from models import FocusSession, Topic
from sqlalchemy import func
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
    output = []

    all_fs = FocusSession.query.filter_by().all()
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

@focus_bp.route('/api/get_topics/<subject>', methods=['GET'])
def get_topics(subject):
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    topics = Topic.query.filter_by(subject=subject).all()


    return jsonify({'status': 'success', 'topics': [{"id": topic.id, "name": topic.name} for topic in topics if topic.name != subject]})
@focus_bp.route('/api/get_subjects', methods=['GET'])
def get_subjects():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    subjects = Topic.query.filter_by(type="subject").all()

    return jsonify({'status': 'success', 'subjects': [{"id": s.id, "name": s.name} for s in subjects]})

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
