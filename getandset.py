from flask import *
from sqlalchemy import *
from sqlmodels import *
import randomprofile as rp
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/main.db'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

def getdb():
    with engine.begin() as conn:
        with SQLSession(conn) as session:
            yield session

def checkEmail(email):
    with getdb() as db:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return -1  # If email exists in the system
        else:
            return 0

def getThreadTitle(id):
    with getdb() as db:
        community = db.query(Community).filter(Community.id == id).first()
        if community:
            return community.title
        else:
            return None

def getCoins(id):
    with getdb() as db:
        user = db.query(User).filter(User.id == id).first()
        if user:
            return user.coins
        else:
            return -1

def setCoins(id, amount, act):
    with getdb() as db:
        user = db.query(User).filter(User.id == id).first()
        if user:
            if act == "plus":
                user.coins += amount
            elif act == "minus":
                user.coins -= amount
            db.add(user)
            db.commit()

def getRequestInfo(requestID, action):
    with getdb() as db:
        requestInfo = db.query(Request).filter(Request.id == requestID).first()
        if request_:
            if action == "userID":
                return str(requestInfo.userID)
            elif action == "state":
                return requestInfo.status
            elif action == "rewards":
                return requestInfo.rewards
        return None

def getUserInfo(userID, action):
    with getdb() as db:
        user = db.query(User).filter(User.id == userID).first()
        if user:
            if action == "userid":
                return str(user.id)
            elif action == "email":
                return user.email
            elif action == "pincode":
                return user.pincode
            elif action == "coins":
                return str(user.coins)
            elif action == "avatar":
                return user.avatar
        return None

def getChatInfo(chatID, action):
    with getdb() as db:
        chat = db.query(Chats).filter(Chats.chatID == chatID).first()
        if chat:
            if action == "srcuser":
                return str(chat.srcUserID)
            elif action == "dstuser":
                return str(chat.dstUserID)
            elif action == "time":
                return str(chat.time)
        return None

def verifyPinCode(id, pincode):
    with getdb() as db:
        user = db.query(User).filter(User.id == id).first()
        if user:
            if user.pincode == pincode:
                return 0
            else:
                return -1
    return -1

def setPassword(id, password):
    with getdb() as db:
        user = db.query(User).filter(User.id == id).first()
        if user:
            user.password = password
            db.add(user)
            db.commit()

def setPinCode(id, pincode):
    with getdb() as db:
        user = db.query(User).filter(User.id == id).first()
        if user:
            user.pincode = pincode
            db.add(user)
            db.commit()

def getItemInfo(itemID, action):
    with getdb() as db:
        shop = db.query(Shop).filter(Shop.id == itemID).first()
        if shop:
            if action == "name":
                return shop.itemName
            elif action == "detail":
                return shop.itemDetail
            elif action == "price":
                return str(shop.price)
        return None

def getTime():
    currentTime = datetime.now()
    composeTime = str(currentTime.year) + "-" + str(currentTime.month) + "-" + str(currentTime.day) + " on " + \
                  str(currentTime.hour) + ":" + str(currentTime.minute) + ":" + str(currentTime.second)
    return composeTime
