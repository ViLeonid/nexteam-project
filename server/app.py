import uuid, os, re
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from gigachat import GigaChat
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from bs4 import BeautifulSoup
from sqlalchemy.ext.mutable import MutableList 

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG") == "True"

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

db = SQLAlchemy(app)
giga = GigaChat(credentials=os.getenv("GIGACHAT_CREDENTIALS"), scope="GIGACHAT_API_PERS", verify_ssl_certs=False)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True, cascade="all, delete-orphan")
    events = db.relationship('Event', backref='user', lazy=True, cascade="all, delete-orphan")

class Todo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, default=False)  
    deadline = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(20), default="blue")
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    todo_id = db.Column(db.String(36), db.ForeignKey('todo.id', ondelete="CASCADE"), nullable=True)
    olympiad_id = db.Column(db.String(36), db.ForeignKey('olympiads.id', ondelete="CASCADE"), nullable=True)
    todo = db.relationship('Todo', backref=db.backref('event', uselist=False, cascade="all, delete-orphan"))

class Olympiads(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subjects = db.Column(MutableList.as_mutable(db.JSON), default=list)
    dates = db.Column(MutableList.as_mutable(db.JSON), default=list)
    url = db.Column(db.String(100))
    classes = db.Column(db.String(20))
    level_perechnya = db.Column(db.String(100))




with app.app_context():
    db.create_all()

def validate_password(password):

    if len(password) < 10:
        return False

    if not re.search(r'[A-Z]', password) and not re.search(r'[А-Я]', password):
        return False

    if not re.search(r'[a-z]', password) and not re.search(r'[а-я]', password):
        return False

    if not re.search(r'\d', password):
        return False

    return True

def parse_datetime(dt_str):
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        return None
    

def map_date(i):
    x=[]
    for j in i.split(' '):
        for k in j.split('-'):
            x.append(k)
    months={
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'мая': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12
    }
    if len(x) == 2:
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month <= months[x[1]]:
            return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'23:59')]
        else:
            return [parse_datetime(str(current_year+1)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'23:59')]
    if len(x) == 3:
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month <= months[x[2]]:
            return [parse_datetime(str(current_year)+'-'+str(months[x[2]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[2]])+'-'+x[1]+'T'+'23:59')]
        else:
            return [parse_datetime(str(current_year+1)+'-'+str(months[x[2]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[2]])+'-'+x[1]+'T'+'23:59')]
    if len(x) == 4:
        current_year = datetime.now().year
        current_month = datetime.now().month
        if current_month <= months[x[1]]:
            if current_month <= months[x[3]]:
                return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]
            else:
                return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]
        else:
            if current_month <= months[x[3]]:
                return [parse_datetime(str(current_year)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]
            else:
                return [parse_datetime(str(current_year+1)+'-'+str(months[x[1]])+'-'+x[0]+'T'+'00:00'), parse_datetime(str(current_year+1)+'-'+str(months[x[3]])+'-'+x[2]+'T'+'23:59')]





def parse_olympiads(limit):
    output_olympiads = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    for activity_id in range(1, limit+1):
        if not Olympiads.query.filter_by(id=activity_id).first():

            try:
                url = f"https://olimpiada.ru/activity/{activity_id}"
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=10
                )
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                h1_tag = soup.find("h1")
                if not h1_tag:
                    continue

                olympiad_name = h1_tag.get_text(strip=True)
                subjects = []
                subject_block = soup.select_one('div.subject_tags_full')

                if subject_block:
                    subjects = subject_block.get_text(
                        separator='/',
                        strip=True
                    ).split('/')

                all_texts = [
                    link.get_text(strip=True)
                    for link in soup.select(
                        f'td a[href^="/activity/{activity_id}/events/"]'
                    )
                ]

                dates = []

                for i in range(0, len(all_texts), 2):
                    if i + 1 < len(all_texts):
                        dates.append({
                            "stage": all_texts[i],
                            "date": all_texts[i + 1]
                                .replace("...", "-")
                                .replace("\xa0", " ")
                        })


                olympiad_site = None

                for svg in soup.select("a svg"):
                    link = svg.parent
                    href = link.get("href")

                    if href and href.startswith("http"):
                        olympiad_site = href
                        break
                if not olympiad_site:
                    olympiad_site=''
                classes = ''
                if soup.find('span', class_='classes_types_a'):
                    classes = soup.find('span', class_='classes_types_a').text.split(' ')[0]
               

                level_perechnya = ""
                blocks = soup.find_all('div', class_='f_blocks')

                # Перебираем все блоки в поиске нужного текста
                for block in blocks:
                    text_perechnya = block.get_text()
                    
                    if "В Перечне Минобрнауки" in text_perechnya:
                        # Ищем слово "уровень" и цифру после него
                        match = re.search(r'уровень\s*(\d+)', text_perechnya)
                        if match:
                            level_perechnya = match.group(1) # Получит "2"
                            break # Выходим из цикла, если нашли


                olympiad = Olympiads(
                    id = activity_id,
                    title = olympiad_name,
                    subjects = subjects,
                    dates = dates,
                    classes = classes,
                    url = olympiad_site,
                    level_perechnya = level_perechnya
                )
                db.session.add(olympiad)
                db.session.commit()    
                this_olympiad = Olympiads.query.filter_by(id=activity_id).first()
                output_olympiads.append({
                    "id": this_olympiad.id,
                    "title": this_olympiad.title,
                    "subjects": this_olympiad.subjects,
                    "dates": this_olympiad.dates,
                    "classes": this_olympiad.classes,
                    "url": this_olympiad.url,
                    "level_perechnya": this_olympiad.level_perechnya
                })
                print(f'{ activity_id } parsed')

            except Exception as e:
                print(activity_id, e)
        else:
            print(f'{ activity_id } was not parsed')
            this_olympiad = Olympiads.query.filter_by(id=activity_id).first()
            output_olympiads.append({
                    "id": this_olympiad.id,
                    "title": this_olympiad.title,
                    "subjects": this_olympiad.subjects,
                    "dates": this_olympiad.dates,
                    "classes": this_olympiad.classes,
                    "url": this_olympiad.url,
                    "level_perechnya": this_olympiad.level_perechnya
                })
    return output_olympiads








@app.route('/api/register', methods=['POST'])
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
                color='purple',
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

@app.route('/todos/<todo_id>', methods=['PUT', 'DELETE'])
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

@app.route('/api/events/<event_id>', methods=['DELETE'])
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
    
@app.route('/api/analytics/today', methods=['GET'])
def get_today_analytics():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    # 1. Определяем границы текущего дня (от 00:00:00 до 23:59:59)
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
    today_end = datetime(now.year, now.month, now.day, 23, 59, 59)

    # 2. Берем события пользователя, которые начинаются СЕГОДНЯ
    events = Event.query.filter(
        Event.user_id == current_user_id,
        Event.start_time >= today_start,
        Event.start_time <= today_end
    ).all()

    if not events:
        return jsonify({
            "labels": ["Свободный день"],
            "values": [24],
            "colors": ["#1f293d"]  # Темный пустой сектор вместо серого
        })

    # Карта цветов для категорий
        # Карта неоновых цветов
    color_map = {
        "blue": {"label": "Обычные дела", "hex": "#00f0ff"},     # Электрический циан
        "red": {"label": "Дедлайны / Задачи", "hex": "#ff007f"},  # Неоновый розовый
        "purple": {"label": "Задачи от ИИ", "hex": "#a020f0"}    # Неоновый фиолетовый
    }

    


    # Словарь для суммирования часов по категориям
    # Пример: { "blue": 2.5, "red": 1.0 }
    duration_stats = {}

    for ev in events:
        color_name = ev.color if ev.color in color_map else "blue"
        
        # Считаем длительность события в часах
        duration_timedelta = ev.end_time - ev.start_time
        duration_hours = duration_timedelta.total_seconds() / 3600.0
        
        # Если событие внезапно имеет некорректное время, берем минимум 30 минут
        if duration_hours <= 0:
            duration_hours = 0.5 

        duration_stats[color_name] = duration_stats.get(color_name, 0.0) + duration_hours

    # 3. Собираем списки для фронтенда
    labels = []
    values = []
    colors = []

    for color_name, hours in duration_stats.items():
        labels.append(color_map[color_name]["label"])
        # Округляем часы до 1 знака после запятой (например, 1.5 часа)
        values.append(round(hours, 1))
        colors.append(color_map[color_name]["hex"])

    return jsonify({
        "labels": labels,
        "values": values,
        "colors": colors
    })

@app.route('/olympiads', methods=['GET'])
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

@app.route('/api/olympiads/parse', methods=['POST'])
def olympiad_parser():
    current_user_id = session.get('user_id')
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    data = request.get_json()
    olympiads = parse_olympiads(int(data.get('count')))
    return jsonify({"status": "success","olympiads": olympiads})

@app.route('/add_olympiad/<olympiad_id>', methods=['POST'])
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
    return jsonify({"status": "success"})
    
if __name__ == '__main__':
    app.run(debug=debug_mode)
