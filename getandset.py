from flask import *
import sqlite3
import datetime as dt
from sqlmodels import *
import randomprofile as rp

app = Flask(__name__)

DATABASE = 'database/main.db'

def get_db():
    dbconnect = getattr(g, '_database', None)
    if dbconnect is None:
        dbconnect = g._database = sqlite3.connect(DATABASE)
    return dbconnect

def checkEmail(email):
    getdb = get_db()
    cursor = getdb.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?",(email,))
    result = cursor.fetchone()
    if result is not None: # If email is exists in the system
        return -1
    else:
        return 0

try:
    @app.route("/api/threadtitle/<id>",methods=["GET"])
    def getThreadTitle(id):
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT title FROM community WHERE threadID=?",(id,))
        result = cursor.fetchone()
        return result[0] # Remove ('')

    def getCoins(id):
        try:
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT coins FROM users WHERE userID=?",(id,))
            result = cursor.fetchone()
            return result[0] # Remove ('')
        except Exception as e:
            print("[ERROR] getCoins: " + str(e))
            return -1
    
    def setCoins(id,amount,act):
        try:
            currentCoins = getCoins(id)
            if act == "plus":
                newCoinAmount = int(currentCoins) + int(amount)
            elif act == "minus":
                newCoinAmount = int(currentCoins) - int(amount)
            else:
                newCoinAmount = int(currentCoins) # Unknown action
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("UPDATE users SET coins=? WHERE userID=?",(newCoinAmount,id))
            getdb.commit()
            return 0
        except Exception as e:
            print("[ERROR] setCoins: " + str(e))
            return -1
        
    def getRequestInfo(requestID,action):
        if action == "userID":
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT userID FROM requests WHERE requestID=?",(requestID,))
            result = cursor.fetchone()
            return result[0]
        elif action == "state":
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT status FROM requests WHERE requestID=?",(requestID,))
            result = cursor.fetchone()
            return result[0]
        elif action == "rewards":
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT rewards FROM requests WHERE requestID=?",(requestID,))
            result = cursor.fetchone()
            return result[0]
        else:
            print("[ERROR] getRequestInfo: Invalid action!")

except Exception as e:
    print("Unexpected error occured.")
    print("Detail: " + str(e))
    exit(-1)
