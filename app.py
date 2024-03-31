from flask import *
import sqlite3

app = Flask(__name__)

DATABASE = 'database/main.db'

def get_db():
    dbconnect = getattr(g, '_database', None)
    if dbconnect is None:
        dbconnect = g._database = sqlite3.connect(DATABASE)
    return dbconnect

@app.route("/")
def hello_world():
    return render_template('index.html')
