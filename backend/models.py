from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

    # relationship
    predictions = db.relationship("Prediction", backref="user", lazy=True)


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    input_data = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    probability = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now)