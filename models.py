from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    subjects = db.relationship('Subject', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    lecture_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    progress = db.relationship('Progress', backref='chapter', lazy=True, uselist=False)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    lectures = db.Column(db.Text)  # JSON string of lecture completion states
    dpp = db.Column(db.Boolean, default=False)
    revision = db.Column(db.Boolean, default=False)
    pyq = db.Column(db.Boolean, default=False)
    tests = db.Column(db.Boolean, default=False)

    def get_lecture_states(self):
        return json.loads(self.lectures) if self.lectures else []

    def set_lecture_states(self, states):
        self.lectures = json.dumps(states)
