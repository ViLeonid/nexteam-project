import uuid
from extensions import db
from sqlalchemy.ext.mutable import MutableList



class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    todos = db.relationship(
        "Todo", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    events = db.relationship(
        "Event", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    focussessions = db.relationship(
        "FocusSession", backref="user", lazy=True, cascade="all, delete-orphan"
    )


class Todo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_done = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)


class Event(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    color = db.Column(db.String(20), default="blue")
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    todo_id = db.Column(
        db.String(36), db.ForeignKey("todo.id", ondelete="CASCADE"), nullable=True
    )
    olympiad_id = db.Column(
        db.String(36), db.ForeignKey("olympiads.id", ondelete="CASCADE"), nullable=True
    )
    todo = db.relationship(
        "Todo", backref=db.backref("event", uselist=False, cascade="all, delete-orphan")
    )


class Olympiads(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subjects = db.Column(MutableList.as_mutable(db.JSON), default=list)
    dates = db.Column(MutableList.as_mutable(db.JSON), default=list)
    url = db.Column(db.String(100))
    classes = db.Column(db.String(20))
    level_perechnya = db.Column(db.String(100))


class FocusSession(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    topic = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(50), nullable=False)
    is_tasks = db.Column(db.Boolean, default=False)
    count_tasks = db.Column(db.Integer, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    real_time = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)


class Topic(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid.uuid4().hex)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.String(36), db.ForeignKey("topic.id"), nullable=True)
    type = db.Column(db.String(20), nullable=False, default="topic")
    children = db.relationship("Topic", backref=db.backref("parent", remote_side=[id]))
