from flask import *
import datetime as dt
from app import *
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "UWA_c1ts_5505_as51gnm3nt2" # Secret Key for all sessions
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1) # All sessions will be destroyed after 24 hrs

def login_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if ifLogin() == -1 or request.cookies.get("session") is None:
                return redirect(url_for('loginPage',errmsg="Please login before accessing function."))
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
