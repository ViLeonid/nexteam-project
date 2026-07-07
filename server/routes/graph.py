from flask import Blueprint, jsonify, request, session
from sqlalchemy import func
from models import db, Topic, FocusSession

graph_bp = Blueprint("graph", __name__)

@graph_bp.get("/api/graph/<subject>")
def get_subject_topics(subject):
    topics = (Topic.query.filter_by(subject=subject).order_by(Topic.name).all())
    return jsonify([
        {
            "id": topic.id,
            "name": topic.name,
            "parent_id": topic.parent_id
        }
        for topic in topics
    ])

@graph_bp.post("/api/graph/topic")
def create_topic():

    data = request.get_json()

    topic = Topic(
        name=data["name"],
        subject=data["subject"],
        parent_id=data.get("parent_id")
    )

    db.session.add(topic)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": topic.id
    })

@graph_bp.delete("/api/graph/topic/<topic_id>")
def delete_topic(topic_id):

    topic = Topic.query.get_or_404(topic_id)

    db.session.delete(topic)
    db.session.commit()

    return jsonify({"success": True})

@graph_bp.get("/api/graph/<subject>/progress")
def get_graph_progress(subject):

    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    hours = (
        db.session.query(
            FocusSession.topic,
            func.sum(FocusSession.real_time)
        )
        .filter(
            FocusSession.user_id == current_user_id,
            FocusSession.subject == subject
        )
        .group_by(FocusSession.topic)
        .all()
    )

    hours_map = {
        topic: round(seconds / 3600, 1)
        for topic, seconds in hours
    }

    topics = Topic.query.filter_by(subject=subject).all()

    result = []

    for topic in topics:

        result.append({

            "id": topic.id,

            "name": topic.name,

            "type": topic.type,

            "parent_id": topic.parent_id,

            "hours": hours_map.get(topic.name, 0)

        })

    return jsonify(result)