import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS



from routes.auth import auth_bp
from routes.todos import todos_bp
from routes.events import events_bp
from routes.analytics import analytics_bp
from routes.olympiads import olympiads_bp
from routes.focus import focus_bp
from routes.graph import graph_bp
from parsing_olympiads import parse_olympiads
from extensions import db

load_dotenv()
app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(todos_bp)
app.register_blueprint(events_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(olympiads_bp)
app.register_blueprint(focus_bp)
app.register_blueprint(graph_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG") == "True"

CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

db.init_app(app)

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=debug_mode)
