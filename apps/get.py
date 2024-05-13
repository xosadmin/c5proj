import os
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from models.sqlmodels import *
from datetime import datetime
import hashlib

app = Flask(__name__)

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

def checkIfUserExist(userID): # For chatroom, check if destination user exists
    user = UserInfo.query.filter(UserInfo.userID == userID).first()
    if user:
          return True
    else:
          return False

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

def ifUserPurchased(userid,itemid): # Check if user already buy the specified item
     result = Transaction.query.filter(and_(Transaction.userID == userid, Transaction.itemID == itemid)).first()
     if result:
          return True # If user already purchased this item
     else:
          return False # If user didn't purchase this item before

def getItemInfo(itemID, action):
        shop = Shop.query.filter(Shop.itemID == itemID).first()
        if shop:
            if action == "detail":
                return shop.itemDetail
            elif action == "price":
                return str(shop.price)
            else:
                 return None
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

def encryptPassword(text):
     md5 = hashlib.md5()
     md5.update(text.encode(encoding='utf-8')) # Encode text as UTF-8
     return str(md5.hexdigest())

def getCountForLeaderboard():
    requestCount = db.session.query(Requests.userID, func.count(Requests.userID).label("requestcount")). \
                    group_by(Requests.userID).subquery()
    todoCount = db.session.query(Todo.userID, func.count(Todo.userID).label("todocount")). \
                    group_by(Todo.userID).subquery()
    # requestCount = return an object that includes userID and its request count
    # todoCount = return an object that includes userID and its accepted request count
    # Both objects are group user by userID to avoid from duplicate count
    # .subquery() = define these queries as sub-query and the main query is required
    return requestCount, todoCount

