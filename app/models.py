from flask_login import UserMixin
from datetime import datetime
from app import db


class Signup(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    profile_picture_url = db.Column(db.String(500))  # stores only url for pfp
    timezone = db.Column(db.String(100), default="Asia/Karachi", nullable=False)

    expenses = db.relationship(
        "Expense", backref="user", cascade="all, delete", passive_deletes=True
    )


class Expense(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(
        db.Integer, db.ForeignKey("signup.id", ondelete="CASCADE"), nullable=False
    )


class Income(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    note = db.Column(db.String(500), nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("signup.id", ondelete="CASCADE"), nullable=False
    )
