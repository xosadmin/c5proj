from flask import *
import datetime as dt
from app import *
import randomprofile as rp
from functools import wraps
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine('sqlite:///your_database.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def login_required(func):
        @wraps(func)
        def logreq(*args, **kwargs):
            encryptedSession = request.cookies.get("session")
            if ifLogin() == -1:
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
        session = Session()
        user_session = UserSession(userid=userid, username=username)
        session.add(user_session)
        session.commit()
        session.close()

def getSession(action):
        session = Session()
        user_session = session.query(UserSession).first()
        session.close()
        if user_session:
                if action == "userid":
                        return user_session.userid
        return None
    
def destroySession():
        session = Session()
        session.query(UserSession).delete()
        session.commit()
        session.close()
