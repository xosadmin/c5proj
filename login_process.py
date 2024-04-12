from flask import *
import datetime as dt
from app import *
import randomprofile as rp
from functools import wraps

app = Flask(__name__)

def login_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            encryptedSession = request.cookies.get("session")
            if ifLogin() == -1 or encryptedSession is None:
                return redirect(url_for('loginPage',errormsg="Please login before accessing function."))
            return func(*args, **kwargs)
        return decorated_function

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
        return str(session.get(action))
    
def destroySession():
        session.clear
