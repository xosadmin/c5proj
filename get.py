import os
from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlmodels import *
import randomprofile as rp
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.getcwd() + '/database/main.dbSession'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
connect = engine.connect()
alchemySession = sessionmaker(bind=engine)

dbSession = alchemySession()

def checkEmail(email):
        user = UserInfo.query.filter(UserInfo.email == email).first()
        if user:
            return -1  # If email exists in the system
        else:
            return 0

def getThreadTitle(id):
        community = Community.query.filter(Community.threadID == id).first()
        if community:
            return community.title
        else:
            return None

def getCoins(id):
        user = UserInfo.query.filter(UserInfo.userID == id).first()
        if user:
            return user.coins
        else:
            return -1

def getRequestInfo(requestID, action):
        requestInfo = Requests.query.filter(Requests.requestID == requestID).first()
        if requestInfo:
            if action == "userID":
                return str(requestInfo.userID)
            elif action == "state":
                return requestInfo.status
            elif action == "rewards":
                return requestInfo.rewards
        return None

def getUserInfo(userID, action):
    user = UserInfo.query.filter(UserInfo.userID == userID).first()
    if user:
        if action == "userid":
            return str(user.userID)
        elif action == "email":
            return user.email
        elif action == "pincode":
            return user.pincode
        elif action == "coins":
            return str(user.coins)
        elif action == "avatar":
            return user.avatar
        else:
             return None
    else:
        return None


def getChatInfo(chatID, action):
        chat = Chats.query.filter(Chats.chatID == chatID).first()
        if chat:
            if action == "srcuser":
                return str(chat.srcUserID)
            elif action == "dstuser":
                return str(chat.dstUserID)
            elif action == "time":
                return str(chat.time)
        return None

def verifyPinCode(id, pincode):
    if "@" in id:
        user = UserInfo.query.filter(UserInfo.email == id).first()
    else:
        user = UserInfo.query.filter(UserInfo.userID == id).first()
    if user:
        if user.pincode == pincode:
                return 0
        else:
                return -1
    return -1

def getItemInfo(itemID, action):
        shop = Shop.query.filter(Shop.itemID == itemID).first()
        if shop:
            if action == "name":
                return shop.itemName
            elif action == "detail":
                return shop.itemDetail
            elif action == "price":
                return str(shop.price)
        return None

def ifSign(userID):
     timeObject = datetime.now()
     currentDay = str(timeObject.year) + "/" + str(timeObject.month) + "/" + str(timeObject.day)
     result = Signs.query.filter(and_(Signs.userID == userID, Signs.time == currentDay)).first()
     if result:
          return True # If the user signed today
     else:
          return False # If the user did not sign today

def getTime():
    currentTime = datetime.now()
    composeTime = str(currentTime.year) + "-" + str(currentTime.month) + "-" + str(currentTime.day) + " on " + \
                  str(currentTime.hour) + ":" + str(currentTime.minute) + ":" + str(currentTime.second)
    return composeTime
