from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')