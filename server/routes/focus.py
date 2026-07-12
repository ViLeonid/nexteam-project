from flask import Blueprint, jsonify, request, session

from utils import parse_datetime_with_seconds
from models import FocusSession, Topic, ActiveFocusSession, Subject
from datetime import datetime
from extensions import db

focus_bp = Blueprint("focus", __name__)


@focus_bp.route("/api/focus_history", methods=["GET"])
def focus():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    output = []

    all_fs = FocusSession.query.filter_by(user_id=current_user_id).all()
    for fs in all_fs:
        output.append(
            {
                "id": fs.id,
                "start_time": fs.start_time,
                "end_time": fs.end_time,
                "subject": fs.subject,
                "real_time": fs.real_time,
                "is_tasks": fs.is_tasks,
                "topic": fs.topic,
                "goal": fs.goal,
                "bg": fs.bg,
                "music": fs.music,
                "count_tasks": fs.count_tasks
            }
        )

    return jsonify({"status": "success", "focus_sessions": output})


@focus_bp.route("/api/active_focus", methods=["GET"])
def get_active_focus():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    active = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()
    if not active:
        return jsonify({"active": False, "focus": {"status": "notstarted"}})
    return jsonify(
        {
            "active": True,
            "focus": {
                "id": active.id,
                "topic": active.topic,
                "goal": active.goal,
                "subject": active.subject,
                "start_time": active.start_time,
                "real_time": active.real_time,
                "work_started_at": active.work_started_at.isoformat(),
                "status": active.status,
                "count_tasks": active.count_tasks,
                "is_tasks": active.is_tasks,
                "bg": active.bg,
                "music": active.music,
            },
        }
    )


# @focus_bp.route("/api/start_fs", methods=["POST"])
# def add_fs():
#     current_user_id = session.get("user_id")
#     if not current_user_id:
#         return jsonify({"error": "Неавторизованный доступ"}), 401
#     fs = request.get_json()
#     new_fs = FocusSession(
#         start_time=parse_datetime_with_seconds(fs.get("start_time")),
#         end_time=parse_datetime_with_seconds(fs.get("end_time")),
#         subject=fs.get("subject"),
#         real_time=fs.get("real_time"),
#         is_tasks=fs.get("is_tasks"),
#         topic=fs.get("topic"),
#         goal=fs.get("goal"),
#         count_tasks=fs.get("count_tasks"),
#         user_id=current_user_id,
#     )
#     db.session.add(new_fs)
#     db.session.commit()
#     return jsonify({"status": "success"})


@focus_bp.route("/api/focus/start", methods=["GET", "POST"])
def start_fs():

    current_user_id = session.get("user_id")

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    if request.method == "POST":

        afs = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()
        if afs:
            print("delete afs")
            db.session.delete(afs)
            db.session.commit()

        fs = request.get_json()

        active_fs = ActiveFocusSession(
            start_time=datetime.now(),
            work_started_at=datetime.now(),
            status="running",
            subject=fs.get("subject"),
            real_time=0,
            is_tasks=fs.get("is_tasks", False),
            topic=fs.get("topic"),
            goal=fs.get("goal"),
            count_tasks=0,
            user_id=current_user_id,
            bg=fs.get("bg"),
            music=fs.get("music")
        )

        db.session.add(active_fs)
        db.session.commit()

        return jsonify({"status": "success", "timer_status": active_fs.status})


    if request.method == "GET":

        active_fs = ActiveFocusSession.query.filter_by(
            user_id=current_user_id
        ).first()

        if not active_fs:
            return jsonify({
                "active": False
            })


        return jsonify({
            "active": True,
            "timer_status": active_fs.status,
            "work_started_at": active_fs.work_started_at.isoformat()
        })

@focus_bp.route("/api/focus/pause", methods=["GET"])
def pause_fs():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401


    active_fs = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()
    active_fs.status = "paused"
    active_fs.real_time += int((datetime.now() - active_fs.work_started_at).total_seconds())
    db.session.add(active_fs)
    db.session.commit()
    return jsonify({"status": "success", "timer_status": active_fs.status})

@focus_bp.route("/api/focus/continue", methods=["GET"])
def continue_fs():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    active_fs = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()
    active_fs.status="running"
    active_fs.work_started_at=datetime.now()

    db.session.add(active_fs)
    db.session.commit()
    return jsonify({"status": "success", "timer_status": active_fs.status, "work_started_at": active_fs.work_started_at.isoformat()})


@focus_bp.route("/api/focus/end", methods=["GET", "POST"])
def end_fs():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    active_fs = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()
    if active_fs.status == "running":
        active_fs.real_time += int(
            (datetime.now()-active_fs.work_started_at)
            .total_seconds()
        )
    new_fs = FocusSession(
        start_time=active_fs.start_time,
        end_time=datetime.now(),
        subject=active_fs.subject,
        real_time=active_fs.real_time,
        is_tasks=active_fs.is_tasks,
        topic=active_fs.topic,
        goal=active_fs.goal,
        count_tasks=active_fs.count_tasks,
        user_id=current_user_id,
        bg=active_fs.bg,
        music=active_fs.music
    )
    db.session.add(new_fs)
    db.session.delete(active_fs)
    db.session.commit()
    return jsonify({"status": "success", "timer_status": "notstarted"})


@focus_bp.route("/api/focus/tasks", methods=["POST"])
def add_tasks():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    data = request.get_json()
    active_fs = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()

    active_fs.count_tasks += data.get("tasks")
    db.session.add(active_fs)
    db.session.commit()
    return jsonify({"status": "success"})


@focus_bp.route("/api/focus/time", methods=["POST"])
def add_time():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    data = request.get_json()
    active_fs = ActiveFocusSession.query.filter_by(user_id=current_user_id).first()

    active_fs.real_time += data.get("time")
    db.session.add(active_fs)
    db.session.commit()
    return jsonify({"status": "success"})


@focus_bp.route("/api/get_topics/<subject>", methods=["GET"])
def get_topics(subject):
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    topics = Topic.query.filter_by(subject=subject).all()

    return jsonify(
        {
            "status": "success",
            "topics": [
                {"id": topic.id, "name": topic.name}
                for topic in topics
                if topic.name != subject
            ],
        }
    )


@focus_bp.route("/api/get_all_subjects", methods=["GET"])
def get_all_subjects():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    subjects = Topic.query.filter_by(type="subject").all()
    return jsonify(
        {
            "status": "success",
            "subjects": [{"id": s.id, "name": s.name} for s in subjects],
        }
    )

@focus_bp.route("/api/get_subjects", methods=["GET"])
def get_subjects():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    subjects = Subject.query.all()
    return jsonify(
        {
            "status": "success",
            "subjects": [{"id": s.id, "name": s.name} for s in subjects],
        }
    )
