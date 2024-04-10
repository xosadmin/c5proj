from flask import *
import sqlite3
import llm
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
        return render_template('community.html')

    @app.route("/requests", methods=["GET"])
    def requestPage():
        return render_template('requests.html')

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
            title = request.form['title']
            content = request.form['content']
            try:
                getdb = get_db() # Create an object to connect to the database
                cursor = getdb.cursor() # Create a cursor to interact with the DB
                cursor.execute("INSERT INTO threads (title,content) VALUES (?,?)",(title,content))
                getdb.commit()
                getdb.close()
                return redirect(url_for('community'))
            except:
                return redirect(url_for('newthread'))
        else:
            return redirect(url_for('newthread'))
    
    @app.route("/donewrequest",methods=['GET','POST'])
    def donewrequests():
        if request.method == "POST":
            title = request.form['title']
            content = request.form['content']
            rewards = request.form['rewards']
            timelimit = request.form['timelimit']
            try:
                getdb = get_db() # Create an object to connect to the database
                cursor = getdb.cursor() # Create a cursor to interact with the DB
                cursor.execute("INSERT INTO users (title,content,rewards,timelimit) VALUES (?,?,?,?)",(title,content,rewards,timelimit))
                getdb.commit()
                getdb.close()
                return redirect(url_for('requests'))
            except:
                return redirect(url_for('newrequest'))
        else:
            return redirect(url_for('newrequest'))
    
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
                return redirect(url_for('profilePage',userid=userid)) # If username and password is correct
            else:
                return redirect(url_for('loginPage', errormsg="Wrong username/password input!"))
        else:
            return redirect(url_for('loginPage', errormsg="Invalid Request!")) # If the user attempts to use GET method to pass the data
    
    @app.route('/profile')
    def profilePage():
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
    def answerRequest():
        return render_template('answerrequest.html',
                               requestid = '',
                               requestTitle = '',
                               requestContent = ''
                               )
    
    @app.route("/todo")
    def todoList():
        return render_template('todo.html', 
                               requestid='',
                               title='',
                               npc=''
                              )

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
