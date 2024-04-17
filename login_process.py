from flask import *
from sqlalchemy import *
import datetime as dt
from app import *
import randomprofile as rp
from functools import wraps

app = Flask(__name__)

def login_required(func):
        @wraps(func)
        def logreq(*args, **kwargs):
            encryptedSession = request.cookies.get("session")
            if ifLogin() == -1 and encryptedSession is None:
                return redirect(url_for('loginPage',errormsg="Please login before accessing function."))
            return func(*args, **kwargs)
        return logreq

def ifLogin():
        tempUserid = getSession("userid")
        if tempUserid is None:
            return -1
        else:
            return 0

def setSession(userid,username):
        session["userid"] = userid
        session["username"] = username

def getSession(action):
        try:
              composeReply = session[action]
        except:
              composeReply = None
        return composeReply
    
def destroySession():
        session.clear()
