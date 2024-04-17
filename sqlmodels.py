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
    
    def getID(self):
        return self.id
    
    def getEmail(self):
        return self.email
    
    def getPassword(self):
        return self.password

    def getCoins(self):
        return self.coins
    
    def getAvatar(self):
        return self.avatar
    
    def getPinCode(self):
        return self.pincode
    
    def setID(self, value):
        self.id = value
    
    def setEmail(self,value):
        self.email = value
    
    def setPassword(self,value):
        self.password = value
    
    def setCoins(self,value):
        self.coins = value

    def setAvatar(self,value):
        self.avatar = value

    def setPincode(self,value):
        self.pincode = value

class Community(Base):
    __tablename__ = 'community'
    id = Column(Text, primary_key=True)
    title = Column(String(120), nullable=False)
    userID = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Community %r>' % self.title
    
    def getid(self):
        return self.id
    
    def getTitle(self):
        return self.title
    
    def getUserID(self):
        return self.userID
    
    def setid(self,value):
        self.id = value

    def setTitle(self,value):
        self.title = value

    def setUserID(self,value):
        self.userID = value

class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Text, primary_key=True)
    userID = Column(Integer, ForeignKey('users.id'))
    contents = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '<Thread %r>' % self.id
    
    def getid(self):
        return self.id

    def setid(self, id):
        self.id = id

    def getuserID(self):
        return self.userID

    def setuserID(self, userID):
        self.userID = userID

    def getcontents(self):
        return self.contents

    def setcontents(self, contents):
        self.contents = contents

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
    
    def getid(self):
        return self.id

    def setid(self, id):
        self.id = id

    def gettitle(self):
        return self.title

    def settitle(self, title):
        self.title = title

    def getcontent(self):
        return self.content

    def setcontent(self, content):
        self.content = content

    def getrewards(self):
        return self.rewards

    def setrewards(self, rewards):
        self.rewards = rewards

    def gettimelimit(self):
        return self.timelimit

    def settimelimit(self, timelimit):
        self.timelimit = timelimit

    def getuserID(self):
        return self.userID

    def setuserID(self, userID):
        self.userID = userID

    def getstatus(self):
        return self.status

    def setstatus(self, status):
        self.status = status

    def getanswer(self):
        return self.answer
    
    def setanswer(self, answer):
        self.answer = answer

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    detail = Column(Text, nullable=False)
    price = Column(Integer, default=0)

    def __repr__(self):
        return '<Shop %r>' % self.id

    def getid(self):
        return self.id

    def setid(self, id):
        self.id = id

    def getdetail(self):
        return self.detail

    def setdetail(self, detail):
        self.detail = detail

    def getprice(self):
        return self.price

    def setprice(self, price):
        self.price = price

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('users.id'))
    itemID = Column(Integer, ForeignKey('shop.id'))

    def __repr__(self):
        return '<Transaction %r>' % self.id
    
    def getid(self):
        return self.id

    def setid(self, id):
        self.id = id

    def getuserID(self):
        return self.userID

    def setuserID(self, userID):
        self.userID = userID

    def getitemID(self):
        return self.itemID

    def setitemID(self, itemID):
        self.itemID = itemID

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userID = Column(Integer, ForeignKey('users.id'))
    requireID = Column(Integer, ForeignKey('requests.id'))
    status = Column(Text, default="Undo")

    def __repr__(self):
        return '<Todo %r>' % self.id
    
    def getid(self):
        return self.id

    def setid(self, id):
        self.id = id

    def getuserID(self):
        return self.userID

    def setuserID(self, userID):
        self.userID = userID

    def getrequireID(self):
        return self.requireID

    def setrequireID(self, requireID):
        self.requireID = requireID

    def getstatus(self):
        return self.status

    def setstatus(self, status):
        self.status = status
    
class Chats(Base):
    __tablename__ = 'chats'
    chatID = Column(Text, primary_key=True)
    srcUserID = Column(Integer, ForeignKey('users.id'))
    dstUserID = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False, default="No Content")

    def __repr__(self):
        return '<Chats %r>' % self.chatID
    
    def getchatID(self):
        return self.chatID

    def setchatID(self, chatID):
        self.chatID = chatID

    def getsrcUserID(self):
        return self.srcUserID

    def setsrcUserID(self, srcUserID):
        self.srcUserID = srcUserID

    def getdstUserID(self):
        return self.dstUserID

    def setdstUserID(self, dstUserID):
        self.dstUserID = dstUserID

    def getcontent(self):
        return self.content

    def setcontent(self, content):
        self.content = content
