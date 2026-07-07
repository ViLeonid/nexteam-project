import json
from pathlib import Path

from app import app
from extensions import db
from models import Topic


TOPICS_DIR = Path(__file__).parent / "topics"


def create_topic(node, subject, parent=None):

    topic = Topic(
        name=node["name"],
        subject=subject,
        type=node.get("type", "topic"),
        parent_id=parent.id if parent else None
    )

    db.session.add(topic)
    db.session.flush()


    for child in node.get("children", []):

        create_topic(
            child,
            subject,
            topic
        )

with app.app_context():

    Topic.query.delete()
    db.session.commit()

    for file in TOPICS_DIR.glob("*.json"):

        print(f"Загружается {file.name}")

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        subject = data["subject"]

        root = Topic(
            name=subject,
            subject=subject,
            type="subject"
        )

        db.session.add(root)
        db.session.flush()

        for node in data["topics"]:
            create_topic(node, subject, root)

    db.session.commit()

print("Все темы успешно импортированы.")