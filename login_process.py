from flask import Flask, session, request, redirect, url_for
import datetime as dt
from app import *
import randomprofile as rp
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = rp.randomSessionKey(16)  # Secret Key for all sessions

def login_required(func):
    @wraps(func)
    def logreq(*args, **kwargs):
        encryptedSession = request.cookies.get("session")
        if ifLogin() == -1 and encryptedSession is None:
            return redirect(url_for('loginPage', errormsg="Please login before accessing function."))
        return func(*args, **kwargs)
    return logreq


def ifLogin():
    tempUserid = getSession("userid")
    if tempUserid is None:
        return -1
    else:
        return 0


def setSession(userid, username):
    session["userid"] = str(userid)
    session["username"] = str(username)


def getSession(action):
    try:
        composeReply = session[action]
    except:
        composeReply = None
    return composeReply


def destroySession():
    session.clear()
