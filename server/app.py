import uuid
from datetime import datetime
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from gigachat import GigaChat
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_batman_key' # ИСПРАВЛЕНО: Ключ для шифрования сессий

# ИСПРАВЛЕНО: Настройка CORS для работы с куками авторизации Vue
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

db = SQLAlchemy(app)
giga = GigaChat(credentials="MDE5ZGRhMzYtODYwZC03MTg5LWEyODQtMmI1NjNmOWU0NWZkOmE0ZDlmYTcwLTFmMTctNDIxZi04ZmFmLWNmZjM1ZTEwYmE4MQ==", scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True, cascade="all, delete-orphan")

class Todo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, default=False)  
    deadline = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

# 1. Добавьте новую модель в Python-код бэкенда
class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False) # Календарные события требуют точное время
    end_time = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(20), default="blue")   # Кастомный цвет для событий
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

# 2. Добавьте связь в модель User (внутри класса User)
# events = db.relationship('Event', backref='user', lazy=True, cascade="all, delete-orphan")

# 3. Создайте роут для получения и создания событий



with app.app_context():
    db.create_all()

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Заполните все поля"}), 400
        
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Этот никнейм уже занят"}), 400
        
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "Регистрация успешна"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id # Записываем сессию
        return jsonify({"status": "success", "message": "Вход выполнен", "username": user.username}), 200
    return jsonify({"error": "Неверное имя пользователя или пароль"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.clear() # Полностью очищаем сессию на сервере
    return jsonify({"status": "success"})

@app.route('/api/events', methods=['GET', 'POST'])
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

    # GET запрос: получаем события пользователя
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

@app.route('/todos', methods=['GET', 'POST'])
def handle_todos():
    # ИСПРАВЛЕНО: Защита роута и получение id текущего юзера
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    if request.method == 'POST':
        data = request.get_json()
        if data.get('subject') is None:
            new_todo = Todo(
                title=data.get('title'),
                description=data.get('description'),
                is_done=data.get('is_done', False),
                deadline=parse_datetime(data.get('deadline')),
                user_id=current_user_id # ИСПРАВЛЕНО: Передаем обязательный внешний ключ
            )
            db.session.add(new_todo)
            db.session.commit()
        else:
            subject = data.get('subject')
            topic = data.get('topic')
            prompt = f"Ты помощник олимпиадника по предмету {subject}. Придумай задачу на сегодня по теме {topic}. Пиши сразу только условие задачи."
            response = giga.chat(prompt)
            content = response.choices[0].message.content
            
            title_text = topic if topic else subject
            new_todo = Todo(
                title=title_text,
                description=content,
                is_done=data.get('is_done', False),
                deadline=parse_datetime(data.get('deadline')),
                user_id=current_user_id # ИСПРАВЛЕНО: Передаем обязательный внешний ключ
            )
            db.session.add(new_todo)
            db.session.commit()
        return jsonify({'status': 'success'})
    
    # ИСПРАВЛЕНО: Забираем задачи ТОЛЬКО текущего залогиненного юзера
    todos = Todo.query.filter_by(user_id=current_user_id).all()
    output = []
    for todo in todos:
        output.append({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'is_done': todo.is_done,
            'deadline': todo.deadline.strftime('%Y-%m-%dT%H:%M') if todo.deadline else None
        })
    return jsonify({'status': 'success', 'todos': output})

@app.route('/todos/<todo_id>', methods=['PUT', 'DELETE'])
def single_todo(todo_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
        
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first_or_404()
    
    if request.method == 'PUT':
        data = request.get_json()
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.is_done = data.get('is_done', todo.is_done)
        if 'deadline' in data:
            todo.deadline = parse_datetime(data.get('deadline'))
        db.session.commit()
        return jsonify({'status': 'success'})
    
    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
