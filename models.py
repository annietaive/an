from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()  # Tạo instance duy nhất của SQLAlchemy

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    progress = db.relationship('Progress', backref='user', lazy=True)

class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    vietnamese = db.Column(db.String(100), nullable=False)
    example = db.Column(db.String(255))
    audio_url = db.Column(db.String(255))  # URL to audio pronunciation

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    options = db.Column(db.String(255))  # Comma-separated options
    difficulty = db.Column(db.String(20), default='basic')  # basic, intermediate, advanced

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    options = db.Column(db.String(255))  # Comma-separated options
    difficulty = db.Column(db.String(20), default='basic')  # basic, intermediate, advanced

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_complete = db.Column(db.Integer, default=0)
    quiz_complete = db.Column(db.Integer, default=0)
    vocabulary_mastered = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)