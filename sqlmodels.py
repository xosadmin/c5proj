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
        return '[ID:{},email:{},coins:{},avatar:{},pincode:{}]'.format(self.id,self.email,self.coins,self.avatar,self.pincode)

class Community(Base):
    __tablename__ = 'community'
    id = Column(Text, primary_key=True)
    title = Column(String(120), nullable=False)
    userID = Column(Integer, ForeignKey('User.id'))

    def __repr__(self):
        return '[ID:{},title:{},userID:{}]'.format(self.id,self.title,self.userID)

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Text, primary_key=True)
    userID = Column(Integer, ForeignKey('User.id'))
    contents = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '[ID:{},userID:{},contents:{}]'.format(self.id,self.userID,self.contents)

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    rewards = Column(String(120))
    timelimit = Column(String(120))
    userID = Column(Integer, ForeignKey('User.id'))
    status = Column(Text, nullable=False, default="Available")
    answer = Column(Text)

    def __repr__(self):
        return '[ID:{},title:{},content:{},rewards:{},timelimit:{},userid:{},status:{},answer:{}]'.format(self.id,
        self.title,self.content,self.rewards,self.timelimit,self.userID,self.status,self.answer)

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    detail = Column(Text, nullable=False)
    price = Column(Integer, default=0)

    def __repr__(self):
        return '[ID:{},detail:{},price:{}]'.format(self.id,self.detail,self.price)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('User.id'))
    itemID = Column(Integer, ForeignKey('Shop.id'))

    def __repr__(self):
        return '[ID:{},userID:{},itemID:{}]'.format(self.id,self.userID,self.itemID)

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('User.id'))
    requireID = Column(Integer, ForeignKey('Request.id'))
    status = Column(Text, default="Undo")

    def __repr__(self):
        return '[ID:{},userID:{},requireID:{},status:{}]'.format(self.id,self.userID,self.requireID,self.status)
    
class Chats(Base):
    __tablename__ = 'chats'
    chatID = Column(Text, primary_key=True)
    srcUserID = Column(Integer, ForeignKey('User.id'))
    dstUserID = Column(Integer, ForeignKey('User.id'))
    content = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '[ID:{},srcUserID:{},dstUserID:{},content:{}]'.format(self.chatID,self.srcUserID,self.dstUserID,self.content)
