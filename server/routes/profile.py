from flask import Blueprint, jsonify, request, session
from models import Subject, User, FocusSession
from datetime import datetime
from utils import validate_password, parse_date
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from collections import defaultdict
from datetime import datetime
import json, os

profile_bp = Blueprint("profile", __name__)

giga = GigaChat(credentials=os.getenv("GIGACHAT_CREDENTIALS"), scope="GIGACHAT_API_PERS", verify_ssl_certs=False)


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
    all_text = current_user.ai_text
    print(current_user.ai_text)
    sentences=[]
    for s in all_text.split('/'):
        sentences.append({"text": s, "checked": False})
    return jsonify({"status": "success", "login": current_user.username, "goal_name": current_user.goal_name, "goal_date": date,
                    "focus_time": current_user.cycle_work_time, "break_time": current_user.cycle_break_time, "auto_start": current_user.auto_start,
                    "ai_text": sentences, "last_ai_date": current_user.last_ai_get})

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

@profile_bp.route("/api/profile/save_focus", methods=["POST"])
def save_focus():
    current_user_id = session.get("user_id")
    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401
    data = request.get_json()
    user = User.query.filter_by(id=current_user_id).first()
    user.cycle_work_time = data.get("focus_time")
    user.cycle_break_time = data.get("break_time")
    user.auto_start = data.get("auto_start")
    db.session.commit()
    return jsonify({"status": "success"})

@profile_bp.route("/api/profile/ai_analytics", methods=["GET"])
def ai_analytics():
    current_user_id = session.get("user_id")

    if not current_user_id:
        return jsonify({"error": "Неавторизованный доступ"}), 401

    now = datetime.now()
    today = now.date()

    user = User.query.filter_by(id=current_user_id).first()
    sessions = FocusSession.query.filter_by(user_id=current_user_id).all()

    total_minutes = 0
    week_minutes = 0
    today_minutes = 0

    subjects = defaultdict(lambda: {
        "minutes": 0,
        "sessions": 0
    })

    for fs in sessions:
        minutes = fs.real_time // 60

        total_minutes += minutes

        if fs.start_time.date() == today:
            today_minutes += minutes

        if (today - fs.start_time.date()).days < 7:
            week_minutes += minutes

        subjects[fs.subject]["minutes"] += minutes
        subjects[fs.subject]["sessions"] += 1


    analytics = {
        "goal": {
            "name": user.goal_name,
            "target_date": (
                user.goal_date.strftime("%Y-%m-%d")
                if user.goal_date else None
            ),
            "days_left": (
                (user.goal_date.date() - today).days
                if user.goal_date else None
            ),
        },

        "focus": {
            "today_minutes": today_minutes,
            "week_minutes": week_minutes,
            "total_minutes": total_minutes,
            "total_sessions": len(sessions),
            "average_session_minutes": (
                total_minutes // len(sessions)
                if sessions else 0
            ),
        },

        "subjects": dict(subjects),

        "pomodoro": {
            "work_minutes": user.cycle_work_time,
            "break_minutes": user.cycle_break_time,
            "auto_start": user.auto_start,
        }
    }


    prompt = f"""
Ты — ИИ-помощник NexTeam для подготовки к олимпиадам и экзаменам.

Текущая дата: {now.strftime("%d.%m.%Y")}
Текущее время: {now.strftime("%H:%M")}

Аналитика пользователя:

{json.dumps(analytics, ensure_ascii=False, indent=2)}


На основе аналитики составь план на день из 5 коротких мини целей на сегодня.

Требования:
- Только 5 пунктов.
- Каждый пункт — один квест для пользователя, чтобы ему хотелось учиться для выполнения всех квестов.
- Почти каждой мини цели должно быть число, чтобы пользователь мог не просто выполнить совет, а осознать свою работу.
- Цели должны быть выпонимыми.
- Пиши кратко, без объяснений, пояснений в скобках и комментариев.
- Учитывай текущий прогресс пользователя.
- Не придумывай факты, которых нет в данных.
- Учитывай текущее время дня.
- После каждого пункта напиши /

Формат:

1. ... /
2. ... /
3. ... /
4. ... /
5. ... /


Пример хорошего ответа:

1. Решить 10 задач по физике./
2. Повторить 2 темы по математике./
3. Выполнить 5 заданий по информатике./
4. Провести 2 фокус-сессии./
5. Разобрать 3 сложные задачи./

Верни только список.
"""

    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.USER,
                content=prompt
            )
        ],
        #model="GigaChat-Max",
        max_tokens=100,
        temperature=1,
    )


    response = giga.chat(payload)

    ai_text = response.choices[0].message.content.strip()

    user = User.query.filter_by(id=current_user_id).first()
    user.ai_text = ai_text
    user.last_ai_get = datetime.now()
    db.session.commit()

    all_text = ai_text.split('/')
    sentences=[]
    for s in all_text:
        sentences.append({"text": s, "checked": False})

    return jsonify({
        "status": "success",
        "output": sentences
    })
