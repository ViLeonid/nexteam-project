from flask import Blueprint, jsonify, request, session
from datetime import timedelta
from gigachat import GigaChat
import os


from models import Todo, Event
from extensions import db
from utils import parse_datetime

todos_bp = Blueprint(
    "todos",
    __name__
)

giga = GigaChat(credentials=os.getenv("GIGACHAT_CREDENTIALS"), scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

@todos_bp.route('/api/todos', methods=['GET', 'POST'])
def handle_todos():
    current_user_id = session.get('user_id')
    if not current_user_id:
        print('sdasdsadasdsad')
        return jsonify({"error": "Неавторизованный доступ"}), 401

    if request.method == 'POST':
        data = request.get_json()
        if data.get('subject') is None:
            new_todo = Todo(
                title=data.get('title'),
                description=data.get('description'),
                is_done=data.get('is_done', False),
                deadline=parse_datetime(data.get('deadline')),
                user_id=current_user_id
            )
            new_event = Event(
                title=data.get('title'),
                description=data.get('description'),
                start_time=parse_datetime(data.get('deadline')),
                end_time=parse_datetime(data.get('deadline')) + timedelta(hours=1),
                color='red',
                user_id=current_user_id,
                todo=new_todo
            )
            db.session.add(new_todo)
            db.session.add(new_event)
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
            new_event = Event(
                title=title_text,
                description=content,
                start_time=parse_datetime(data.get('deadline')),
                end_time=parse_datetime(data.get('deadline')) + timedelta(hours=1),
                color='red',
                user_id=current_user_id,
                todo=new_todo
            )
            db.session.add(new_todo)
            db.session.add(new_event)
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

@todos_bp.route('/api/todos/<todo_id>', methods=['PUT', 'DELETE'])
def single_todo(todo_id):
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first_or_404()
    if request.method == 'PUT':
        data = request.get_json()
        new_title=data.get('title')
        if not new_title or new_title.strip() == "":
            return jsonify({"error": "Название задачи не может быть пустым"}), 400
        todo.title = new_title
        todo.description = data.get('description', todo.description)
        todo.is_done = data.get('is_done', todo.is_done)
        if 'deadline' in data:
            todo.deadline = parse_datetime(data.get('deadline'))
        if todo.event:
            todo.event.title = todo.title
            todo.event.description = todo.description
            if todo.deadline:
                todo.event.start_time = todo.deadline
                todo.event.end_time = todo.deadline + timedelta(hours=1)
        todo.event.color = 'green' if todo.is_done else 'red'
        db.session.commit()
        return jsonify({'status': 'success'})

    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'status': 'success'})