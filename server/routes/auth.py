from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import User
from extensions import db
from utils import validate_password

auth_bp = Blueprint(
    "auth",
    __name__
)
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Заполните все поля"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Этот никнейм уже занят"}), 400
    if not validate_password(password):
        return jsonify({"error": "Пароль не соответсвует требованиям"}), 400
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "Регистрация успешна"}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id # Записываем сессию
        return jsonify({"status": "success", "message": "Вход выполнен", "username": user.username}), 200
    return jsonify({"error": "Неверное имя пользователя или пароль"}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear() # Полностью очищаем сессию на сервере
    return jsonify({"status": "success"})