import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.getcwd() + '/database/main.db'
db = SQLAlchemy()

class UserInfo(db.Model):
    __tablename__ = 'users'
    userID = Column(String(120), primary_key=True)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    coins = Column(Integer, nullable=False, default=10)
    avatar = Column(Text, nullable=False, default="default")
    country = Column(Text, nullable=False)
    pincode = Column(Text, nullable=False, default="123")

    def __repr__(self):
        return '[ID:{}, email:{}, coins:{}, avatar:{}, pincode:{}]'.format(self.userID, self.email, self.coins, self.avatar, self.pincode)

class Community(db.Model):
    __tablename__ = 'community'
    threadID = Column(Text, primary_key=True)
    title = Column(String(120), nullable=False)
    userID = Column(Integer, ForeignKey('users.userID'))

    def __repr__(self):
        return '[ID:{},title:{},userID:{}]'.format(self.threadID,self.title,self.userID)

class Thread(db.Model):
    __tablename__ = 'threads'
    replyID = Column(Integer, primary_key=True, autoincrement=True)
    threadID = Column(Text, nullable=False)
    userID = Column(Integer, ForeignKey('users.userID'))
    contents = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '[ID:{},userID:{},contents:{}]'.format(self.threadID,self.userID,self.contents)

class Requests(db.Model):
    __tablename__ = 'requests'
    requestID = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    rewards = Column(String(120))
    timelimit = Column(String(120))
    userID = Column(Integer, ForeignKey('users.userID'))
    status = Column(Text, nullable=False, default="Available")
    answer = Column(Text)

    def __repr__(self):
        return '[ID:{},title:{},content:{},rewards:{},timelimit:{},userid:{},status:{},answer:{}]'.format(self.requestID,
        self.title,self.content,self.rewards,self.timelimit,self.userID,self.status,self.answer)

class Shop(db.Model):
    __tablename__ = 'shop'
    itemID = Column(Integer, primary_key=True)
    itemDetail = Column(Text, nullable=False)
    price = Column(Integer, default=0)

    def __repr__(self):
        return '[ID:{},detail:{},price:{}]'.format(self.itemID,self.itemDetail,self.price)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transactionID = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('users.userID'))
    itemID = Column(Integer, ForeignKey('shop.itemID'))

    def __repr__(self):
        return '[ID:{},userID:{},itemID:{}]'.format(self.transactionID,self.userID,self.itemID)

class Todo(db.Model):
    __tablename__ = 'todo'
    todoID = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('users.userID'))
    requestID = Column(Integer, ForeignKey('requests.requestID'))
    status = Column(Text, default="Undo")

    def __repr__(self):
        return '[ID:{},userID:{},requireID:{},status:{}]'.format(self.todoID,self.userID,self.requestID,self.status)
    
class Chats(db.Model):
    __tablename__ = 'chats'
    replyID = Column(Integer, primary_key=True, autoincrement=True)
    chatID = Column(Text, nullable=False)
    srcUserID = Column(Integer, ForeignKey('users.userID'))
    dstUserID = Column(Integer, ForeignKey('users.userID'))
    content = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '[ID:{},srcUserID:{},dstUserID:{},content:{}]'.format(self.chatID,self.srcUserID,self.dstUserID,self.content)

class Signs(db.Model):
    __tablename__ = 'signs'
    signID = Column(Text, primary_key=True)
    userID = Column(Text, nullable=False)
    time = Column(Text, nullable=False)
    emotion = Column(Text, nullable=False, default="Happy")
    comments = Column(Text, nullable=False, default="No Comment")
    rewards = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return '[signID:{},userID:{},time:{},emotion:{},comments:{},rewards:{}]'.format(self.signID,self.userID,
                                                                                        self.time,self.emotion,self.comments,self.rewards)
    