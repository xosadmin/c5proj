from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    coins = db.Column(db.Integer, default=10)

    def __repr__(self):
        return '<User %r>' % self.email

class Thread(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userID'))

    def __repr__(self):
        return '<Thread %r>' % self.title

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rewards = db.Column(db.String(120))
    timelimit = db.Column(db.String(120))

    def __repr__(self):
        return '<Request %r>' % self.title

class Shop(db.Model):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Shop %r>' % self.name

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
    requireID = db.Column(db.Integer, db.ForeignKey('requests.requestID'))
    Status = db.Column(db.Text, default="Undo")

    def __repr__(self):
        return '<Todo %r>' % self.requireID