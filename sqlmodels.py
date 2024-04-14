from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    coins = Column(Integer, nullable=False, default=10)
    avatar = Column(Text, nullable=False, default="default")
    pincode = Column(Text, nullable=False, default="123")

    def __repr__(self):
        return '<User %r>' % self.email

class Community(Base):
    __tablename__ = 'community'
    id = Column(Text, primary_key=True)
    title = Column(String(120), nullable=False)
    userID = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Community %r>' % self.title

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Text, primary_key=True)
    userID = Column(Integer, ForeignKey('users.id'))
    contents = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '<Thread %r>' % self.id

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    rewards = Column(String(120))
    timelimit = Column(String(120))
    userID = Column(Integer, ForeignKey('users.id'))
    status = Column(Text, nullable=False, default="Available")
    answer = Column(Text)

    def __repr__(self):
        return '<Request %r>' % self.title

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    detail = Column(Text, nullable=False)
    price = Column(Integer, default=0)

    def __repr__(self):
        return '<Shop %r>' % self.id

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('users.id'))
    itemID = Column(Integer, ForeignKey('shop.id'))

    def __repr__(self):
        return '<Transaction %r>' % self.id

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('users.id'))
    requireID = Column(Integer, ForeignKey('requests.id'))
    status = Column(Text, default="Undo")

    def __repr__(self):
        return '<Todo %r>' % self.id
    
class Chats(Base):
    __tablename__ = 'chats'
    chatID = Column(Text, primary_key=True)
    srcUserID = Column(Integer, ForeignKey('users.id'))
    dstUserID = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '<Chats %r>' % self.chatID
