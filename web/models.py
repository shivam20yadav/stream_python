from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
class feedback(db.Model):
    feed_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    message = db.Column(db.String(10000))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(200))

