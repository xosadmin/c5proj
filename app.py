from flask import *
import sqlite3
import llm
from sqlmodels import *
import randomprofile as rp
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/main.db'
db.init_app(app)

DATABASE = 'database/main.db'

def get_db():
    dbconnect = getattr(g, '_database', None)
    if dbconnect is None:
        dbconnect = g._database = sqlite3.connect(DATABASE)
    return dbconnect

def checkEmail(email):
    getdb = get_db()
    cursor = getdb.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?",(email))
    result = cursor.fetchone()
    if result is not None: # If email is exists in the system
        return -1
    else:
        return 0

try:
    @app.route("/")
    def homepage():
        return render_template('index.html')

    @app.route("/login", methods=["GET"])
    def loginPage():
        if request.method == "GET":
            errormsg = request.args.get('errormsg', '')
            return render_template('login.html', errormsg=errormsg)
        else:
            return render_template('login.html')

    @app.route("/register", methods=["GET"])
    def registerPage():
        if request.method == "GET":
            errormsg = request.args.get('errormsg', '')
            return render_template('register.html', errormsg=errormsg)
        else:
            return render_template('register.html')

    @app.route("/community", methods=["GET"])
    def communityPage():
        try:
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM community")
            result = cursor.fetchall()
            getdb.close()
            return render_template('community.html', result=result)
        except Exception as e:
            print(e)
            return render_template('community.html', errmsg="Internal Error")

    @app.route("/requests", methods=["GET"])
    def requestPage():
        try:
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM requests")
            result = cursor.fetchall()
            getdb.close()
            return render_template('requests.html', result=result)
        except Exception as e:
            print(e)
            return render_template('requests.html', errmsg="Internal Error")

    @app.route("/shop")
    def shopPage():
        return render_template('shop.html')
    
    @app.route("/newthread")
    def newThread():
        return render_template('newthread.html')
    
    @app.route("/newrequest")
    def newRequest():
        return render_template('newrequest.html', balance='0')
    
    @app.route("/logout")
    def logoutPage():
        return render_template('logout.html')
    
    @app.route("/donewthread",methods=['GET','POST'])
    def donewthreads():
        if request.method == "POST":
            userID = "1"
            title = request.form['title']
            content = request.form['content']
            try:
                threadUUID = str(uuid.uuid4())
                getdb = get_db() # Create an object to connect to the database
                cursor = getdb.cursor() # Create a cursor to interact with the DB
                cursor.execute("INSERT INTO community (threadID,title,userID) VALUES (?,?,?)",(threadUUID,title,userID))
                cursor.execute("INSERT INTO threads (threadID,userID,contents) VALUES (?,?,?)",(threadUUID,userID,content))
                getdb.commit()
                getdb.close()
                return redirect(url_for('communityPage'))
            except Exception as e:
                print(e)
                return redirect(url_for('newThread', errmsg="Internal Error"))
        else:
            return redirect(url_for('newThread', errmsg="Invalid Request!"))
    
    @app.route("/donewrequest",methods=['GET','POST'])
    def donewrequests():
        if request.method == "POST":
            userID = "1"
            title = request.form['title']
            content = request.form['content']
            rewards = request.form['rewards']
            timelimit = request.form['timelimit']
            try:
                getdb = get_db() # Create an object to connect to the database
                cursor = getdb.cursor() # Create a cursor to interact with the DB
                cursor.execute("INSERT INTO requests (title,content,rewards,timelimit,userID) VALUES (?,?,?,?,?)",(title,content,rewards,timelimit,userID))
                getdb.commit()
                getdb.close()
                return redirect(url_for('requests'))
            except:
                return redirect(url_for('newRequest', errmsg="Internal Error"))
        else:
            return redirect(url_for('newRequest', errmsg="Invalid Request!"))
    
    @app.route("/doregister",methods=['GET','POST'])
    def doregister():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            try:
                checkEmailExist = checkEmail(email)
                if checkEmailExist == 0:
                    getdb = get_db() # Create an object to connect to the database
                    cursor = getdb.cursor() # Create a cursor to interact with the DB
                    cursor.execute("INSERT INTO users (email,password,coins) VALUES (?,?,10)",(email,password))
                    getdb.commit()
                    getdb.close()
                    return render_template("register_complete.html")
                else:
                    return redirect(url_for('registerPage', errormsg="Email already exists"))
            except:
                return redirect(url_for('registerPage', errormsg="An error occurred"))
        else:
            return redirect(url_for('registerPage', errormsg="Invalid request"))
    
    @app.route("/dologin",methods=['GET','POST'])
    def dologin():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            getdb = get_db() # Create an object to connect to the database
            cursor = getdb.cursor() # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password))
            result = cursor.fetchone()
            getdb.close()
            if result:
                userid = result[0] # The first column in the result
                return redirect(url_for('profilePage', userid=userid)) # If username and password is correct
            else:
                return redirect(url_for('loginPage', errormsg="Wrong username/password input!"))
        else:
            return redirect(url_for('loginPage', errormsg="Invalid Request!")) # If the user attempts to use GET method to pass the data
        
    @app.route("/docommsearch", methods=['GET', 'POST'])
    def doCommSearch():
        if request.method == "POST":
            keyword = request.form['keyword']  # assuming the form field is named 'keyword'
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM community WHERE threadID=? OR title=?", (keyword, keyword))
            result = cursor.fetchall()
            getdb.close()
            if result:
                return render_template("search_result.html", act="thread", result=result, infomsg=f"We have found result(s) based on your keyword '{keyword}'")
            else:
                return render_template("search_result.html", errmsg=f"We cannot find any content based on keyword '{keyword}'")
        else:
            return render_template("search_result.html", errmsg="Invalid Request!")
        
    @app.route("/doreqsearch", methods=['GET', 'POST'])
    def doReqSearch():
        if request.method == "POST":
            keyword = request.form['keyword']  # assuming the form field is named 'keyword'
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM requests WHERE requestID=? OR title=?", (keyword, keyword))
            result = cursor.fetchall()
            getdb.close()
            if result:
                return render_template("search_result.html", act="answerrequest", result=result, infomsg=f"We have found result(s) based on your keyword '{keyword}'")
            else:
                return render_template("search_result.html", errmsg=f"We cannot find any content based on keyword '{keyword}'")
        else:
            return render_template("search_result.html", errmsg="Invalid Request!")
    
    @app.route('/profile/<userid>', methods=["GET"])
    def profilePage(id):
        return render_template('profile.html',
                               email='1@1.com',
                               nickname=rp.randomNickname(),
                               location=rp.randomCountry(),
                               coins='0',
                               nftid='1',
                               nftname='test',
                               RewardID='1',
                               RewardName='test'
                               )
    
    @app.route('/answerrequest/<requestid>')
    def answerRequest(requestid):
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM requests WHERE requestID=?", (requestid,))
        result = cursor.fetchone()
        getdb.close()
        if result:
            return render_template("answerrequest.html", result=result)
        else:
            return render_template("answerrequest.html", errmsg=f"We cannot find any content.")
        
    @app.route("/doanswerrequest", methods=['POST'])
    def doAnswerRequest():
        requestID = request.form['requestID']
        content = request.form['content']
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("UPDATE requests SET status='Completed', answer=? WHERE requestID=?", (content,requestID))
        cursor.execute("UPDATE todo SET Status='Completed' WHERE requireID=?", (requestID))
        getdb.commit()
        getdb.close()
        return redirect(url_for('todoList',infomsg="You have completed the request."))
    
    @app.route("/thread/<id>", methods=['GET'])
    def threadDetails(id):
        id = request.args.get('id')  # assuming the form field is named 'keyword'
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM threads WHERE threadID=?", (id,))
        result = cursor.fetchall()
        getdb.close()
        if result:
            return render_template("thread_details.html", result=result)
        else:
            return render_template("thread_details.html", errmsg=f"We cannot find any content.")
    
    @app.route("/acceptrequest/<id>", methods=['GET'])
    def acceptRequest(id):
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM requests WHERE requestID=?", (id,))
        result = cursor.fetchone()
        getdb.close()
        if result:
            return render_template("accept_request.html", result=result)
        else:
            return render_template("accept_request.html", errmsg=f"We cannot find any content.")
        
    @app.route("/requestdetails/<id>", methods=['GET'])
    def requestDetails(id):
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM requests WHERE requestID=?", (id,))
        result = cursor.fetchone()
        getdb.close()
        if result:
            return render_template("requestDetail.html", result=result)
        else:
            return render_template("requestDetail.html", errmsg=f"We cannot find any content.")
        
    @app.route("/doacceptrequest/<id>", methods=['GET'])
    def doAcceptRequest(id):
        userid = "1"
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("UPDATE requests SET status='accepted' WHERE requestID=?", (id,))
        cursor.execute("INSERT INTO todo (userID,requireID,Status) VALUES (?,?,?)", (userid,id,"Accepted"))
        getdb.commit()
        getdb.close()
        return redirect(url_for('todoList'))

    @app.route("/todo")
    def todoList():
        userID = "1"
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM todo WHERE userID=?", (userID))
        result = cursor.fetchall()
        getdb.close()
        if result:
            return render_template("todo.html", result=result)
        else:
            return render_template("todo.html", errmsg=f"We cannot find any content.")

    @app.route("/rewards/<username>")
    def rewardPage():
        return render_template('rewards.html', username='username')
    
    @app.route("/api/llmrequest")
    def llmreq():
        return llm.llmRequests()
    
    @app.route("/api/llmanswer")
    def llmans():
        return llm.llmAnswers()

except Exception as e:
    print("File missing. Cannot proceed. Exiting system...")
    print("Details: " + str(e))
    exit(-1)
# If file is missing, the program cannot start

if __name__ == "__main__":
    app.run()
