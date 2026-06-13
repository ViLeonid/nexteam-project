from flask import Blueprint, jsonify, request, session


from models import Event
from extensions import db
from utils import parse_datetime

events_bp = Blueprint(
    "events",
    __name__
)
@events_bp.route('/api/events', methods=['GET', 'POST'])
def handle_events():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    if request.method == 'POST':
        data = request.get_json()
        new_event = Event(
            title=data.get('title'),
            description=data.get('description'),
            start_time=parse_datetime(data.get('start_time')),
            end_time=parse_datetime(data.get('end_time')),
            color=data.get('color', 'blue'),
            user_id=current_user_id
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'status': 'success', 'id': new_event.id}), 201

    events = Event.query.filter_by(user_id=current_user_id).all()
    output = []
    for ev in events:
        output.append({
            'id': ev.id,
            'title': ev.title,
            'description': ev.description,
            'start_time': ev.start_time.strftime('%Y-%m-%dT%H:%M'),
            'end_time': ev.end_time.strftime('%Y-%m-%dT%H:%M'),
            'color': ev.color
        })
    return jsonify({'status': 'success', 'events': output})



@events_bp.route('/api/events/<event_id>', methods=['DELETE'])
def single_event(event_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    event = Event.query.filter_by(id=event_id, user_id=current_user_id).first_or_404()
    todo = event.todo

    if request.method == 'DELETE':
        db.session.delete(event)
        if todo:
            db.session.delete(todo)
        db.session.commit()
        return jsonify({'status': 'success'})