from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()


class TS_User(db.Model, UserMixin):
    __tablename__ = 'TS_User'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    token = db.Column(db.String(255))
    TS_Task = db.relationship("TS_Task", back_populates="TS_User")


class TS_Task(db.Model):
    __tablename__ = 'TS_Task'
    tid = db.Column(db.Integer, primary_key=True)
    did = db.Column(db.Integer)
    uid1 = db.Column(db.Integer, db.ForeignKey('TS_User.id'))
    uid2 = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    kstatus = db.Column(db.Integer, default=0)
    private = db.Column(db.Boolean, default=False)
    TS_User = db.relationship("TS_User", back_populates="TS_Task")