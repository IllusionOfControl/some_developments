from app import db
from datetime import datetime
import uuid


def _generate_slug():
    return uuid.uuid4().hex


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Text(32), nullable=False, default=_generate_slug, unique=True)
    content = db.Column(db.Text, nullable=False)
    create_timestamp = db.Column(db.DateTime, default=datetime.now())
    expiration_timestamp = db.Column(db.DateTime, default=datetime.min)
