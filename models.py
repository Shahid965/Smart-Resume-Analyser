from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Default avatar set to a professional 'Avataaars' style
    avatar_url = db.Column(db.String(255), default='https://api.dicebear.com/7.x/avataaars/svg?seed=Felix')
    history = db.relationship('ResumeHistory', backref='owner', lazy=True)

class ResumeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100))
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))