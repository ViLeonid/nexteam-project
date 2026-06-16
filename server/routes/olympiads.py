from flask import Blueprint, jsonify, request, session


from models import Olympiads, Event
from extensions import db
from utils import map_date

olympiads_bp = Blueprint(
    "olympiads",
    __name__
)

@olympiads_bp.route('/olympiads', methods=['GET'])
def olympiads():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    all_olympiads = Olympiads.query.filter_by().all()
    output = []
    for this_olympiad in all_olympiads:
            output.append({
                    "id": this_olympiad.id,
                    "title": this_olympiad.title,
                    "subjects": this_olympiad.subjects,
                    "dates": this_olympiad.dates,
                    "classes": this_olympiad.classes,
                    "url": this_olympiad.url,
                    "level_perechnya": this_olympiad.level_perechnya
                })
    return jsonify({'status': 'success', 'olympiads': output})


@olympiads_bp.route('/add_olympiad/<olympiad_id>', methods=['POST'])
def add_olympiad(olympiad_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    olympiad = Olympiads.query.filter_by(id = olympiad_id).first()

    for date in olympiad.dates:
        new_event = Event(
            title=olympiad.title,
            description=date['stage'],
            start_time=map_date(date['date'])[0],
            end_time=map_date(date['date'])[1],
            color='orange',
            olympiad_id = olympiad.id,
            user_id=current_user_id
        )
        db.session.add(new_event)
    db.session.commit()
    print(olympiad.dates)
    return jsonify({"status": "success"})

@olympiads_bp.route('/remove_olympiad/<olympiad_id>', methods=['DELETE'])
def remove_olympiad(olympiad_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
         return jsonify({"error": "Неавторизованный доступ"}), 401
    Event.query.filter_by( olympiad_id=olympiad_id, user_id=current_user_id ).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"status": "success"})

@olympiads_bp.route('/added_olympiads', methods=['GET'])
def added_olympiads():
    current_user_id = session.get('user_id')

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    events = Event.query.filter_by(
        user_id=current_user_id
    ).all()

    olympiad_ids = list({
        event.olympiad_id
        for event in events
        if event.olympiad_id is not None
    })

    return jsonify({
        "status": "success",
        "olympiads": olympiad_ids
    })