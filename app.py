from flask import *
import llm
from sqlmodels import *
from getandset import *
from login_process import *
import randomprofile as rp
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/main.db'
app.config['SECRET_KEY'] = rp.randomSessionKey(16) # Secret Key for all sessions
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1) # All sessions will be destroyed after 24 hrs
db.init_app(app)

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
    @login_required
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

    @app.route("/requests")
    @login_required
    def requestPage():
        try:
            currentUserID = getSession("userid")
            coins = getCoins(currentUserID)
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM requests")
            result = cursor.fetchall()
            getdb.close()
            return render_template('requests.html', result=result, coins=coins, userid=currentUserID)
        except Exception as e:
            print(e)
            return render_template('requests.html', errmsg="Internal Error")

    @app.route("/shop",methods=["GET"])
    @login_required
    def shopPage():
        userID = getSession("userid")
        currentCoin = getCoins(userID)
        return render_template('shop.html',coins=currentCoin)
    
    @app.route("/newthread")
    @login_required
    def newThread():
        return render_template('newthread.html')
    
    @app.route("/newrequest",methods=["GET"])
    @login_required
    def newRequest():
        msg = request.args.get('msg', 'null')
        userID = getSession("userid")
        currentCoin = getCoins(userID)
        return render_template('newrequest.html', balance=currentCoin,msg=msg)
    
    @app.route("/logout")
    @login_required
    def logoutPage():
        destroySession()
        response = make_response(render_template('logout.html'))
        response.set_cookie('session','',expires=0)
        return response
    
    @app.route("/donewthread",methods=['GET','POST'])
    @login_required
    def donewthreads():
        if request.method == "POST":
            userID = getSession("userid")
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
                return "<script>alert('New thread recorded.');window.location.href='/community';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('newThread', errmsg="Internal Error"))
        else:
            return redirect(url_for('newThread', errmsg="Invalid Request!"))

    @app.route("/donewthreadreply", methods=['GET', 'POST'])
    @login_required
    def doNewThreadReply():
        if request.method == "POST":
            userID = getSession("userid")
            content = request.form['content']
            threadUUID = request.form['threadID']
            try:
                getdb = get_db()  # Create an object to connect to the database
                cursor = getdb.cursor()  # Create a cursor to interact with the DB
                cursor.execute("INSERT INTO threads (threadID,userID,contents) VALUES (?,?,?)",
                               (threadUUID, userID, content))
                getdb.commit()
                getdb.close()
                return "<script>alert('New reply recorded.');window.location.href='/thread/"+ threadUUID +"';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('newThread', errmsg="Internal Error"))
        else:
            return redirect(url_for('newThread', errmsg="Invalid Request!"))
    
    @app.route("/donewrequest",methods=['GET','POST'])
    @login_required
    def donewrequests():
        if request.method == "POST":
            userID = getSession("userid")
            currentCoins = getCoins(userID)
            title = request.form['title']
            content = request.form['content']
            rewards = request.form['rewards']
            timelimit = request.form['timelimit']
            if int(rewards) <= int(currentCoins):
                try:
                    getdb = get_db() # Create an object to connect to the database
                    cursor = getdb.cursor() # Create a cursor to interact with the DB
                    cursor.execute("INSERT INTO requests (title,content,rewards,timelimit,userID) VALUES (?,?,?,?,?)",(title,content,rewards,timelimit,userID))
                    getdb.commit()
                    setCoins(userID,int(rewards),"minus")
                    getdb.close()
                    return "<script>alert('New request posted.');window.location.href='/requests';</script>"
                except Exception as e:
                    print("[ERROR] donewrequests: " + str(e))
                    return redirect(url_for('newRequest', msg="Internal Error!"))
            else:
                return redirect(url_for('newRequest', msg="Insufficient Balance!"))
        else:
            return redirect(url_for('newRequest', msg="Invalid Request!"))

    @app.route("/doregister", methods=['GET', 'POST'])
    def doregister():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            try:
                checkEmailExist = checkEmail(email)
                if checkEmailExist == 0:
                    getdb = get_db()  # Create an object to connect to the database
                    cursor = getdb.cursor()  # Create a cursor to interact with the DB
                    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email,password))
                    getdb.commit()
                    getdb.close()
                    return render_template("register_complete.html")
                else:
                    return redirect(url_for('registerPage', errormsg="Email already exists"))
            except Exception as e:
                print(e)
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
                setSession(userid,email)
                return redirect(url_for('profilePage', userid=userid, infomsg="Welcome back to Adventurers Guild!")) # If username and password is correct
            else:
                return redirect(url_for('loginPage', errormsg="Wrong username/password input!"))
        else:
            return redirect(url_for('loginPage', errormsg="Invalid Request!")) # If the user attempts to use GET method to pass the data
        
    @app.route("/docommsearch", methods=['GET', 'POST'])
    @login_required
    def doCommSearch():
        if request.method == "POST":
            keyword = request.form['keyword'].strip()  # assuming the form field is named 'keyword'
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM community WHERE threadID LIKE ? COLLATE NOCASE OR title LIKE ? COLLATE NOCASE", ('%'+keyword+'%', '%'+keyword+'%'))
            result = cursor.fetchall()
            getdb.close()
            if result:
                return render_template("search_result.html", act="thread", result=result, redosearch="docommsearch", infomsg=f"We have found result(s) based on your keyword '{keyword}'")
            else:
                return render_template("search_result.html", errmsg=f"We cannot find any content based on keyword '{keyword}'")
        else:
            return render_template("search_result.html", errmsg="Invalid Request!")
        
    @app.route("/doreqsearch", methods=['GET', 'POST'])
    @login_required
    def doReqSearch():
        if request.method == "POST":
            keyword = request.form['keyword'].strip()  # assuming the form field is named 'keyword'
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("SELECT * FROM requests WHERE requestID LIKE ? COLLATE NOCASE OR title LIKE ? COLLATE NOCASE ", ('%' + keyword + '%', '%' + keyword + '%'))
            result = cursor.fetchall()
            getdb.close()
            if result:
                return render_template("search_result.html", act="answerrequest", result=result, redosearch="doreqsearch", infomsg=f"We have found result(s) based on your keyword '{keyword}'")
            else:
                return render_template("search_result.html", errmsg=f"We cannot find any content based on keyword '{keyword}'")
        else:
            return render_template("search_result.html", errmsg="Invalid Request!")
    
    @app.route('/profile')
    @login_required
    def profilePage():
        try:
            infomsg = request.args.get('infomsg', '')
            userID = getSession("userid")
            getdb = get_db()
            cursor = getdb.cursor()
            rcountry = rp.randomCountry()
            rnickname = rp.randomNickname()
            cursor.execute("SELECT * FROM users WHERE userID=?", (userID,)) # User Info
            user_details = cursor.fetchall()
            if user_details is None:
                return render_template('profile.html', errmsg="User not found")
            cursor.execute("SELECT *  FROM transactions WHERE userID=?", (userID,)) # NFT Images
            nft_details = cursor.fetchall()
            avatar_id = str(getUserInfo(userID,"avatar"))
            getdb.close()
            return render_template('profile.html',
                                user_details = user_details,
                                nft_details = nft_details,
                                rcountry = rcountry,
                                rnickname = rnickname,
                                nftid = avatar_id,
                                infomsg = infomsg
                                )
        except Exception as e:
            print(f"An error occurred: " + str(e))
            return render_template('profile.html', errmsg="An internal error occurred")

    @app.route('/answerrequest/<requestid>')
    @login_required
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
    @login_required
    def doAnswerRequest():
        userID = request.form["userID"]
        rewards = request.form["rewards"]
        requestID = request.form['requestID']
        content = request.form['content']
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("UPDATE requests SET status='Completed', answer=? WHERE requestID=?", (content,requestID))
        cursor.execute("UPDATE todo SET Status='Completed' WHERE requireID=?", (requestID,))
        setCoins(userID,rewards,"plus") # Automatically add coins to adventurers
        getdb.commit()
        getdb.close()
        return redirect(url_for('todoList',infomsg="You have completed the request."))
    
    @app.route("/thread/<id>", methods=['GET'])
    @login_required
    def threadDetails(id):
        thread_title = getThreadTitle(id)
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM threads WHERE threadID=?", (id,))
        result = cursor.fetchall()
        getdb.close()
        if result:
            return render_template("thread_details.html", result=result, threadID=id, threadName=thread_title)
        else:
            return render_template("thread_details.html", errmsg=f"We cannot find any content.")
    
    @app.route("/acceptrequest/<id>", methods=['GET'])
    @login_required
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

    @app.route("/deleterequest/<userid>/<requestid>", methods=['GET'])
    @login_required
    def deleteRequest(userid,requestid):
        currentuserID = getSession("userid")
        state = getRequestInfo(requestid,"state")
        currentReqRewards = getRequestInfo(requestid,"rewards")
        if int(userid) == int(currentuserID) and state == "Available": # Only userID matches and status is Available can delete
            getdb = get_db()  # Create an object to connect to the database
            cursor = getdb.cursor()  # Create a cursor to interact with the DB
            cursor.execute("DELETE FROM requests WHERE requestID=?", (requestid,))
            getdb.commit()
            setCoins(currentuserID,int(currentReqRewards),"plus") # Refund reward if delete request
            getdb.close()
            return "<script>alert('Request Deleted Successfully. Your reward has been refunded.');window.location.href='/requests';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/requests';</script>"

    @app.route("/myrequest")
    @login_required
    def myRequest():
        userID = getSession("userid")
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM requests WHERE userID=?",(userID))
        result = cursor.fetchall()
        getdb.close()
        if result:
            return render_template("myrequest.html", result=result)
        else:
            return render_template("myrequest.html", errmsg=f"We cannot find any content.")

    @app.route("/requestdetails/<id>", methods=['GET'])
    @login_required
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
    @login_required
    def doAcceptRequest(id):
        userID = getSession("userid")
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("UPDATE requests SET status='accepted' WHERE requestID=?", (id,))
        cursor.execute("INSERT INTO todo (userID,requireID,Status) VALUES (?,?,?)", (userID,id,"Accepted"))
        getdb.commit()
        getdb.close()
        return redirect(url_for('todoList'))

    @app.route("/todo")
    @login_required
    def todoList():
        currentUserID = getSession("userid")
        coins = getCoins(currentUserID)
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM todo WHERE userID=?", (currentUserID,))
        result = cursor.fetchall()
        getdb.close()
        if result:
            return render_template("todo.html", result=result, coins=coins)
        else:
            return render_template("todo.html", errmsg=f"We cannot find any content.", coins=coins)
        
    @app.route("/leaderboard")
    @login_required
    def leaderBoard():
        getdb = get_db()  # Create an object to connect to the database
        cursor = getdb.cursor()  # Create a cursor to interact with the DB
        cursor.execute("SELECT * FROM users ORDER BY coins DESC")
        result = cursor.fetchall()
        getdb.close()
        if result:
            return render_template("leaderboard.html", result=result)
        else:
            return render_template("leaderboard.html", errmsg=f"We cannot find any content.")
    
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
