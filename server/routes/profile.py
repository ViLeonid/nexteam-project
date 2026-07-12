from flask import Blueprint, jsonify, request, session
from models import Subject, User
from datetime import datetime
from utils import validate_password, parse_date
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/api/profile/get_subjects", methods=["GET"])
def get_subjects():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    output = []
    for s in Subject.query.filter_by(user_id=current_user_id):
        output.append({
            "id": s.id,
            "name": s.name
        })
    return jsonify({"status": "success", "subjects": output})

@profile_bp.route("/api/profile/add_subject", methods=["POST"])
def add_subject():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    data = request.get_json()
    new_subject = Subject(
        name=data.get('subject'),
        user_id=current_user_id
    )
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({"status": "success","subject":{"id":new_subject.id, "name":new_subject.name}})

@profile_bp.route("/api/profile/delete_subject/<string:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    del_subject = Subject.query.filter_by(user_id=current_user_id, id = subject_id).first()
    db.session.delete(del_subject)
    db.session.commit()
    return jsonify({"status": "success"})

@profile_bp.route("/api/profile", methods=["GET"])
def profile():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    current_user = User.query.filter_by(id=current_user_id).first()
    print(current_user.goal_name)
    date = None
    print(current_user.goal_date)
    if current_user.goal_date:
        date = current_user.goal_date.isoformat()[:10]
    return jsonify({"status": "success", "login": current_user.username, "goal_name": current_user.goal_name, "goal_date": date})

@profile_bp.route('/api/profile/change_password', methods=['POST'])
def change_password():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    data = request.get_json()
    currentPassword = data.get('currentPassword')
    newPassword = data.get('newPassword')
    current_user = User.query.filter_by(id=current_user_id).first()
    if not currentPassword or not newPassword:
        return jsonify({"error": "Заполните все поля"}), 400
    if check_password_hash(current_user.password, generate_password_hash(currentPassword)):
        return jsonify({"error": "Введите верный текущий пароль"}), 400
    if not validate_password(newPassword):
        return jsonify({"error": "Новый пароль не соответсвует требованиям"}), 400
    current_user.password = generate_password_hash(newPassword)
    db.session.commit()
    return jsonify({"status": "success"}), 201

@profile_bp.route("/api/profile/change_goal", methods=["POST"])
def change_goal():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    data = request.get_json()
    user = User.query.filter_by(id=current_user_id).first()
    user.goal_name = data.get("name")
    user.goal_date = parse_date(data.get("date"))
    db.session.commit()
    return jsonify({"status": "success"})