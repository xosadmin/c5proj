import os
from flask import *
import apps.llm as llm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models.sqlmodels import *
from models.formModels import *
from models.loginModels import *
from apps.get import *
from apps.randomprofile import *

migrate = Migrate(app, db) # Create a flask db migration
login_manager = LoginManager()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = randomSessionKey(16) # Secret Key for all sessions
    if config is not None:
        app.config.update(config)
    else: 
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'database', 'main.db')
    db.init_app(app) # Create a new instance. db has been defined in sqlmodel.py
    login_manager.init_app(app) # Create a new Login manager
    login_manager.login_view = "loginPage" # Default Login View
    return app

app = create_app()

try:
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route("/index")
    @app.route("/")
    def homepage():
        if current_user.is_authenticated:
            return redirect(url_for('profilePage',infomsg="You have already logged in. Welcome Back!"))
        else:
            return render_template('index.html')

    @app.route("/login", methods=["GET"])
    def loginPage():
        form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('profilePage',infomsg="You have already logged in. Welcome Back!"))
        else:
            if request.method == "GET":
                errormsg = request.args.get('errormsg', '')
                return render_template('login.html', errormsg=errormsg, form=form)
            else:
                return render_template('login.html',form=form)

    @app.route("/register", methods=["GET", "POST"])
    def registerPage():
        form = RegisterForm()
        if current_user.is_authenticated:
            return redirect(url_for('profilePage',infomsg="You have already logged in. Welcome Back!"))
        else:
            if request.method == "POST": # If user triggered register button
                userID = str(uuidGen())
                email = form.email.data
                password = form.password.data
                repeat_password = form.repeat_password.data
                country = str(randomCountry())
                pincode = form.pin_code.data
                try:
                    checkEmailExist = checkEmail(email)
                    if checkEmailExist == 0 or password != repeat_password: 
                        # Check if the email is registered & Avoid from user that trying to bypass Javascript
                        encryptedPassword = encryptPassword(password)
                        insert = UserInfo(userID=userID,email=email,password=encryptedPassword,country=country,pincode=pincode)
                        db.session.add(insert)
                        db.session.commit()
                        return render_template("register_complete.html")
                    else:
                        return redirect(url_for('registerPage', errormsg="Email already exists or password mismatch"))
                except Exception as e:
                    print(e)
                    return redirect(url_for('registerPage', errormsg="An error occurred"))
            else:
                errormsg = request.args.get('errormsg', '')
                return render_template('register.html', errormsg=errormsg, form=form)
        
    @app.route("/forgetpassword", methods=["GET","POST"])
    def forgetPassword():
        form = ForgetPasswordForm()
        if not current_user.is_authenticated: # If user is not logged in
            if request.method == "POST": # If user trigger Submit button on the frontend
                email = form.email.data
                pincode = form.pin_code.data
                fetchEmail = checkEmail(email)
                if fetchEmail == -1:
                    pin_verify_result = verifyPinCode(email, pincode) # Verify if user's inputed PIN code is correct
                    if pin_verify_result == 0: # If it's correct
                        try:
                            encryptedPassword = encryptPassword("123")
                            db.session.execute(update(UserInfo).filter(UserInfo.email == email).values(password=encryptedPassword))
                            db.session.commit()
                            return "<script>alert('Your password has been reset to: 123.');window.location.href='/login';</script>"
                        except Exception as e:
                            print(f"Error resetting password: {str(e)}") # Print error detail in the console
                            return redirect(url_for('forgetPassword', infomsg="Failed to reset password due to system error."))
                    else: # If it's not incorrect
                        return redirect(url_for('forgetPassword', infomsg="Incorrect PIN."))
                else: # If the backend cannot find the user
                    return redirect(url_for('forgetPassword', infomsg="User not found."))
            else:
                infomsg = request.args.get('infomsg','')
                return render_template('forget_password.html', errormsg=infomsg, form=form)
        else:
            errormsg = "You cannot perform this request while signed in."
            return redirect(url_for('profilePage', infomsg=errormsg))
            # If user is logged in, this function is disabled until logout
    
    @app.route("/modifycenter",methods=["GET","POST"])
    @login_required
    def modifyCentre():
        if request.method == "POST": # If user triggered submit button
            userID = current_user.id # Fetch current logged in user ID
            changeType = request.form["type"]
            if changeType == "email":
                newemail = request.form["newEmail"]
                db.session.execute(update(UserInfo).where(UserInfo.userID==userID).values(email=newemail))
            elif changeType == "country":
                country = request.form["country"]
                db.session.execute(update(UserInfo).where(UserInfo.userID==userID).values(country=country))
            elif changeType == "pin":
                OldpinCode = request.form["oldpin"]
                newpin = request.form["newpin"]
                verifyPinCodeResult = verifyPinCode(userID,OldpinCode) # Verify provided PIN code
                if verifyPinCodeResult == 0: # If it's right
                    db.session.execute(update(UserInfo).where(UserInfo.userID==userID).values(pincode=newpin))
                else: # If it's wrong
                    return render_template("change_profile.html",infomsg="Invalid Old PIN Code!")
            elif changeType == "password":
                pinCode = request.form["pin-code"]
                newpassword = request.form["newpassword"]
                encNewPassword = encryptPassword(newpassword)
                verifyPinCodeResult = verifyPinCode(userID,pinCode)
                if verifyPinCodeResult == 0:
                    db.session.execute(update(UserInfo).where(UserInfo.userID==userID).values(password=encNewPassword))
                else:
                    return render_template("change_profile.html",infomsg="Invalid PIN Code!")
            else:
                return render_template("change_profile.html",infomsg="Invalid Change!")
            db.session.commit()
            return redirect(url_for("profilePage",infomsg="Information " + changeType + " has been updated."))
        else:
            return render_template("change_profile.html")

    @app.route("/community", methods=["GET"])
    @login_required
    def communityPage():
        userID = current_user.id # Fetch current logged in user ID
        try:
            result = Community.query.all() # Fetch all data from Community
            return render_template('community.html', result=result, userID=userID)
        except Exception as e:
            print(e) # Print error in the console
            return render_template('community.html', errmsg="Internal Error")
        
    @app.route("/chat")
    @login_required
    def chatPage():
        userID = current_user.id # Fetch current logged in user ID
        infomsg = request.args.get("infomsg","")
        result = Chats.query.filter(or_(Chats.dstUserID == userID, Chats.srcUserID == userID)).all()
            # Fetch all sent or received chat data for current logged in user
        if result:
            return render_template('chat.html', results=result, infomsg=infomsg)
        else:
            return render_template('chat.html', infomsg="No chat. Do you want to set up a new one?")

    @app.route("/chat/<chatid>")
    @login_required
    def chatDetailsPage(chatid):
        dstuser = getChatInfo(chatid,"dstuser") # Fetch destination user for reply form
        result = Chats.query.join(UserInfo, Chats.srcUserID == UserInfo.userID). \
                add_columns(UserInfo.avatar, Chats.srcUserID, Chats.content). \
                filter(Chats.chatID == chatid).all()
            # Using inner join to fetch userinfo for both side, contents and their avatar
        if result:
            return render_template('chat_details.html',results=result, dstUser=dstuser, chatID=chatid)
        else:
            return render_template('chat_details.html', infomsg="Unexpected error")
        
    @app.route("/dochatreply",methods=['GET','POST'])
    @login_required
    def doChatReply():
        if request.method == "POST": # If user triggered send button on the reply chat page
            userID = current_user.id
            chatID = request.form['chatID']
            content = request.form['content']
            dstuser = request.form['dstUser']
            try:
                insert = Chats(chatID=chatID,srcUserID=userID,dstUserID=dstuser,content=content)
                db.session.add(insert)
                db.session.commit()
                return "<script>alert('Message sent.');window.location.href='/chat/" + chatID + "';</script>"
                # Prompt dialog to notify Message sent to user
            except Exception as e:
                print(e) # Print detailed error on the console
                return redirect(url_for('chatPage', errmsg="Internal Error"))
        else:
            return redirect(url_for('chatPage', errmsg="Invalid Request!"))
        
    @app.route("/deletechat/<chatid>", methods=['GET'])
    @login_required
    def deleteChat(chatid):
        currentuserID = current_user.id
        dstuser = getChatInfo(chatid,"dstuser") # Fetch chat destination user
        srcuser = getChatInfo(chatid,"srcuser") # Fetch chat source user
        if dstuser == currentuserID or srcuser == currentuserID: # Only userID matches src or dst can delete
            db.session.execute(delete(Chats).where(Chats.chatID == chatid))
            db.session.commit()
            return "<script>alert('Your chat has been deleted.');window.location.href='/chat';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/chat';</script>"

    @app.route("/deletethread/<threaduserid>/<threadID>", methods=['GET'])
    @login_required
    def deleteThread(threaduserid,threadID):
        currentuserID = current_user.id
        if threaduserid == currentuserID: # Only userID matches can delete
            db.session.execute(delete(Thread).where(Thread.threadID == threadID))
            db.session.execute(delete(Community).where(Community.threadID == threadID))
            db.session.commit()
            return "<script>alert('Your thread has been deleted.');window.location.href='/community';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/community';</script>"
        
    @app.route("/newchat",methods=['GET','POST'])
    @login_required
    def donewchat():
        form = newChatForm()
        if request.method == "POST":
            chatUUID = str(uuidGen()) # Generate unique UUID for ticket session
            userID = current_user.id
            dstuser = form.dstUser.data
            content = form.contents.data
            checkIfDstExist = checkIfUserExist(dstuser) # Check if destination user exists
            if checkIfDstExist and str(userID) != dstuser:
                try:
                    insert = Chats(chatID=chatUUID,srcUserID=userID,dstUserID=dstuser,content=content)
                    db.session.add(insert)
                    db.session.commit()
                    return "<script>alert('New ticket recorded.');window.location.href='/chat';</script>"
                except Exception as e:
                    print(e) # Print detailed error on the console
                    return redirect(url_for('chatPage', errmsg="Internal Error"))
            else:
                return render_template("newchat.html", form=form, infomsg="Invalid Destination User!")
        else:
            return render_template("newchat.html", form=form)

    @app.route("/newchat/<dstuserid>", methods=['GET'])
    @login_required
    def donewchatwithID(dstuserid):
        form = newChatForm()
        return render_template("newchat.html", dstuserid=dstuserid, form=form)

    @app.route("/requests")
    @login_required
    def requestPage():
        try:
            currentUserID = current_user.id
            coins = getCoins(currentUserID)
            result = Requests.query.all() # Fetch all requests from DB
            return render_template('requests.html', result=result, coins=coins, userid=currentUserID)
        except Exception as e:
            print(e) # Print detailed error on the console
            return render_template('requests.html', errmsg="Internal Error")

    @app.route("/shop",methods=["GET"])
    @login_required
    def shopPage():
        userID = current_user.id
        currentCoin = getCoins(userID) # Fetch coins amount that current user have
        infomsg = request.args.get("infomsg","") # Fetch information message, if exists
        result = Shop.query.all() # Fetch all items from the DB
        if result:
            return render_template('shop.html',coins=currentCoin,results=result, infomsg=infomsg)
        else:
            return render_template('shop.html', coins=currentCoin, infomsg="Unexpected error")
    
    @app.route("/signs",methods=["POST","GET"])
    @login_required
    def signPage():
        form = signEmotionForm()
        signSessionID = uuidGen() # Generate unique UUID for each sign session
        userID = current_user.id
        timeObject = datetime.now()
        currentDay = str(timeObject.year) + "/" + str(timeObject.month) + "/" + str(timeObject.day) # Get current date based on server timezone
        currentCoin = getCoins(userID)
        infomsg = request.args.get("infomsg","")
        ifSigned = ifSign(userID)
        if request.method == "POST": # If user click on submit button
            feelings = form.feelings.data
            comments = form.comments.data
            if not ifSigned: # If user didn't signs today
                try:
                    randomRewards = int(randomCoinRewards())
                    rewardCoins = randomRewards + int(currentCoin) # Generate random rewards and add to user's coins
                    insert = Signs(signID=signSessionID,userID=userID,time=currentDay,emotion=feelings,comments=comments,rewards=randomRewards)
                    db.session.add(insert)
                    db.session.execute(update(UserInfo).where(UserInfo.userID==userID).values(coins=rewardCoins))
                    db.session.commit()
                    return redirect(url_for('profilePage',infomsg="Signed successfully! Welcome back and you have get " 
                                            + str(randomRewards) + " coins for reward!"))
                except Exception as e:
                    print("[ERROR] SignPage: " + str(e))
                    return render_template('signs.html',infomsg="Internal Error! <a href='/profile' title='Profile'>Click here for your profile</a>",
                                           form=form)
            else: # If user signed today and try to sign second time
                return render_template('signs.html',infomsg="You have signed today! <a href='/profile' title='Profile'>Click here for your profile</a>",
                                       form=form)
        else:
            return render_template('signs.html',infomsg=infomsg,form=form)

    @app.route("/newthread",methods=["GET","POST"])
    @login_required
    def newThread():
        form = newThreadForm()
        if request.method == "POST":
            userID = current_user.id
            title = form.title.data
            content = form.contents.data
            try:
                threadUUID = str(uuidGen()) # GEnerate unique UUID for thread
                inserts = [Community(threadID=threadUUID,title=title,userID=userID),
                           Thread(threadID=threadUUID,userID=userID,contents=content)]
                # Community = Record metadata for the thread, Thread = Save conversations related to the thread
                for item in inserts:
                    db.session.add(item)
                db.session.commit()
                return "<script>alert('New thread recorded.');window.location.href='/community';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('newThread', errmsg="Internal Error"))
        else:
            return render_template('newthread.html',form=form)
    
    @app.route("/newrequest",methods=["GET","POST"])
    @login_required
    def newRequest():
        form = newRequestForm()
        if request.method == "POST": # User triggered submit button
            userID = current_user.id
            currentCoins = getCoins(userID)
            title = form.title.data
            content = form.contents.data
            rewards = form.rewards.data
            timelimit = form.timelimit.data
            if int(rewards) <= int(currentCoins): # If user's coin is enough to pay for rewards
                insert = Requests(title=title,content=content,rewards=rewards,timelimit=timelimit,userID=userID)
                remainCoins = int(currentCoins) - int(rewards) # Deduct rewards from user account
                coins = update(UserInfo).filter(UserInfo.userID == userID).values(coins=remainCoins)
                db.session.add(insert)
                db.session.execute(coins)
                db.session.commit()
                return "<script>alert('New request posted.');window.location.href='/requests';</script>"
            else: # If user's coin is not enough to pay for rewards
                return redirect(url_for('newRequest', msg="Insufficient Balance!"))
        else:
            msg = request.args.get('msg', '')
            userID = current_user.id
            currentCoin = getCoins(userID)
            return render_template('newrequest.html', balance=currentCoin,msg=msg,form=form)
    
    @app.route("/logout")
    @login_required
    def logoutPage():
        logout_user() # Logout user and destroy session
        return render_template('logout.html')

    @app.route("/donewthreadreply", methods=['GET', 'POST'])
    @login_required
    def doNewThreadReply():
        if request.method == "POST": # If user triggered on submit button
            userID = current_user.id
            content = request.form['content']
            threadUUID = request.form['threadID']
            try:
                insert = Thread(threadID=threadUUID,userID=userID,contents=content)
                db.session.add(insert)
                db.session.commit()
                return "<script>alert('New reply recorded.');window.location.href='/thread/"+ threadUUID +"';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('newThread', errmsg="Internal Error"))
        else:
            return redirect(url_for('newThread', errmsg="Invalid Request!"))

    @app.route("/dologin",methods=['GET','POST'])
    def dologin():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            encryptedPassword = encryptPassword(password) # encode input password to MD5
            result = UserInfo.query.filter(UserInfo.email == email, UserInfo.password == encryptedPassword).first()
            # Retrieve user info based on provided username and encrypted password
            if result:
                userid = str(result.userID)
                user = User(userid)
                print("[Info] User " + userid + " has login in.")
                login_user(user)
                if ifSign(userid): # If the user signed today
                    return redirect(url_for('profilePage', userid=userid, infomsg="Welcome back to Adventurers Guild!")) # If username and password is correct
                else:
                    return redirect(url_for('signPage'))
            else:
                return redirect(url_for('loginPage', errormsg="Wrong username/password input!"))
        else:
            return redirect(url_for('loginPage', errormsg="Invalid Request!")) # If the user attempts to use GET method to pass the data
        
    @app.route("/docommsearch", methods=['GET', 'POST'])
    @login_required
    def doCommSearch():
        if request.method == "POST":
            keyword = request.form['keyword'].strip()  # The form field is named 'keyword'
            result = Community.query.filter(or_(Community.threadID.ilike('%' + keyword + '%'), 
                        Community.title.ilike('%' + keyword + '%')))
                # use ilike to enable fuzzy search
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
            keyword = request.form['keyword'].strip()  # The form field is named 'keyword'
            result = Requests.query.filter(or_(Requests.requestID.ilike('%' + keyword + '%'), 
                        Requests.title.ilike('%' + keyword + '%')))
                # use ilike to enable fuzzy search
            if result:
                return render_template("search_result.html", act="answerrequest", result=result, redosearch="doreqsearch", infomsg=f"We have found result(s) based on your keyword '{keyword}'")
            else:
                return render_template("search_result.html", errmsg=f"We cannot find any content based on keyword '{keyword}'")
        else:
            return render_template("search_result.html", errmsg="Invalid Request!")
        
    @app.route("/dochatsearch", methods=['GET', 'POST'])
    @login_required
    def doChatSearch():
        if request.method == "POST":
            keyword = request.form['keyword'].strip()  # The form field is named 'keyword'
            result = Chats.query.filter(or_(Chats.srcUserID.ilike('%' + keyword + '%'), 
                        Chats.dstUserID.ilike('%' + keyword + '%')))
                # Use ilike to enable fuzzy search
            if result:
                return render_template("search_result.html", act="chat", result=result, redosearch="dochatsearch", infomsg=f"We have found result(s) based on your keyword '{keyword}'")
            else:
                return render_template("search_result.html", errmsg=f"We cannot find any content based on keyword '{keyword}'")
        else:
            return render_template("search_result.html", errmsg="Invalid Request!")
    
    @app.route('/profile')
    @login_required
    def profilePage():
        try:
            infomsg = request.args.get('infomsg', '')
            userID = current_user.id
            pincode = getUserInfo(userID, "pincode")
            user_details = UserInfo.query.filter(UserInfo.userID == userID).all()  # User Info
            if user_details is None:
                return render_template('profile.html', errmsg="User not found")
            nft_details = Transaction.query.filter(Transaction.userID==userID).all()
            signHistory = Signs.query.filter(Signs.userID == userID).all()
            nftid = str(getUserInfo(userID, "avatar"))  # Get avatar ID
            if "-" in userID: # If "-" is in the userID
                userID_Show_On_Browser = userID.split("-")[0] # Get the first part of the UUID
            else:
                userID_Show_On_Browser = userID
            return render_template('profile.html',
                                userID=userID,
                                userID_Show_On_Browser=userID_Show_On_Browser,
                                user_details=user_details,
                                nft_details=nft_details,
                                nftid=nftid,
                                pincode=pincode,
                                signHistory=signHistory,
                                infomsg=infomsg
                                )
        except Exception as e:
            print(f"An error occurred: " + str(e))
            return render_template('profile.html', errmsg="An internal error occurred")
        
    @app.route('/profile/<userid>') # User profile in 3rd user view
    @login_required
    def profilePageOthersView(userid):
        try:
            infomsg = request.args.get('infomsg', '')
            userID = userid
            if "-" in userID:
                userID_Show_On_Browser = userID.split("-")[0]
            else:
                userID_Show_On_Browser = userID
            user_details = UserInfo.query.filter(UserInfo.userID == userID).all()
            if user_details is None:
                return "<script>alert('Cannot find this user');history.back();</script>"
            avatar_id = str(getUserInfo(userID,"avatar"))
            return render_template('profile_other_user_view.html',
                                userID_Show_On_Browser = userID_Show_On_Browser,
                                userID = userID,
                                user_details = user_details,
                                nftid = avatar_id,
                                infomsg = infomsg
                                )
        except Exception as e:
            print(f"An error occurred: " + str(e))
            return "<script>alert('Internal Error!');history.back();</script>"

    @app.route('/answerrequest/<requestid>')
    @login_required
    def answerRequest(requestid):
        userID = current_user.id
        result = Requests.query.filter(Requests.requestID == requestid).first()
        if result:
            return render_template("answerrequest.html", result=result, userID=userID)
        else:
            return render_template("answerrequest.html", errmsg=f"We cannot find any content.")

    @app.route("/doanswerrequest", methods=['POST'])
    @login_required
    def doAnswerRequest():
        userID = request.form["userID"]
        rewards = request.form["rewards"]
        requestID = request.form['requestID']
        content = request.form['content']
        currentCoins = getUserInfo(userID, "coins")
        remainCoins = int(currentCoins) + int(rewards)
        updates = [update(Requests).where(Requests.requestID == requestID).values(status="Completed",answer=content),
                    update(Todo).where(Todo.requestID == requestID).values(status="Completed"),
                    update(UserInfo).filter(UserInfo.userID == userID).values(coins=remainCoins)]
            # Update Request = Record answer from adventurer; Update Todo = change the request state to complete;
            # Update UserInfo = Add reward to user's wallet
        for item in updates:
            db.session.execute(item)
        db.session.commit()
        return redirect(url_for('todoList',infomsg="Thank you! You have completed the request."))

    @app.route("/thread/<id>", methods=['GET'])
    @login_required
    def threadDetails(id):
        thread_title = getThreadTitle(id)
        result = Thread.query.join(UserInfo, Thread.userID == UserInfo.userID). \
                add_columns(UserInfo.avatar, Thread.userID, Thread.contents). \
                filter(Thread.threadID == id).all()
            # Show UserID, contents and user's avatar based on inner join
        if result:
            return render_template("thread_details.html", result=result, threadID=id, threadName=thread_title)
        else:
            return render_template("thread_details.html", errmsg=f"We cannot find any content.")
    
    @app.route("/acceptrequest/<id>", methods=['GET'])
    @login_required
    def acceptRequest(id):
        result = Requests.query.filter(Requests.requestID == id).first() # Get the request details
        if result:
            return render_template("accept_request.html", result=result)
        else:
            return render_template("accept_request.html", errmsg=f"We cannot find any content.")   
        
    @app.route("/confirmpayment/<id>", methods=['GET'])
    @login_required
    def confirmPayment(id):
        result = Shop.query.filter(Shop.itemID == id).first() # Get the item details
        if result:
            return render_template("confirm_buy.html", result=result)
        else:
            return render_template("confirm_buy.html", errmsg=f"We cannot find any content.")   

    @app.route("/deleterequest/<userid>/<requestid>", methods=['GET'])
    @login_required
    def deleteRequest(userid,requestid):
        currentuserID = current_user.id
        state = getRequestInfo(requestid,"state")
        currentCoins = getUserInfo(userid,"coins")
        currentReqRewards = getRequestInfo(requestid,"rewards")
        remainCoins = int(currentCoins) + int(currentReqRewards) # Refund coins
        if userid == currentuserID and state == "Available": # Only userID matches and status is Available can delete
            commands = [delete(Requests).where(Requests.requestID == requestid),
                        update(UserInfo).filter(UserInfo.userID == userid).values(coins=remainCoins)]
            for item in commands:
                db.session.execute(item)
            db.session.commit()
            return "<script>alert('Request Deleted Successfully. Your reward has been refunded.');window.location.href='/requests';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/requests';</script>"

    @app.route("/myrequest")
    @login_required
    def myRequest():
        userID = current_user.id
        result = Requests.query.filter(Requests.userID == userID).all() # Show all requests that current user posted
        if result:
            return render_template("myrequest.html", result=result)
        else:
            return render_template("myrequest.html", errmsg=f"We cannot find any content.")

    @app.route("/requestdetails/<id>", methods=['GET'])
    @login_required
    def requestDetails(id):
        result = Requests.query.filter(Requests.requestID == id).first()
        if result:
            return render_template("requestDetail.html", result=result)
        else:
            return render_template("requestDetail.html", errmsg=f"We cannot find any content.")
        
    @app.route("/doacceptrequest/<id>", methods=['GET'])
    @login_required
    def doAcceptRequest(id):
        userID = current_user.id
        updateReq = update(Requests).where(Requests.requestID == id).values(status="accepted") # Change the request state to accepted
        insertTodo = Todo(userID=userID,requestID=id,status="Accepted") # Update this request to user's todo list
        db.session.execute(updateReq)
        db.session.add(insertTodo)
        db.session.commit()
        return redirect(url_for('todoList'))

    @app.route("/setavatar/<id>", methods=['GET'])
    @login_required
    def doSetAvatar(id):
        userID = current_user.id
        updateusr = update(UserInfo).where(UserInfo.userID == userID).values(avatar=id) # Set the avatar with specific ID for current user
        db.session.execute(updateusr)
        db.session.commit()
        return redirect(url_for('profilePage',infomsg="Avatar updated."))
    
    @app.route("/dopayment/<id>", methods=['GET'])
    @login_required
    def doPayment(id):
        userID = current_user.id
        itemPrice = getItemInfo(id,"price")
        userCoins = getUserInfo(userID,"coins")
        remainCoins = int(userCoins) - int(itemPrice)
        checkWarehouse = ifUserPurchased(userID,id) # Check if user already purchased this item
        if remainCoins >= 0:
            if not checkWarehouse:
                insert = Transaction(userID=userID,itemID=id)
                db.session.add(insert)
                db.session.execute(update(UserInfo).filter(UserInfo.userID == userID).values(coins=remainCoins))
                db.session.commit()
                return redirect(url_for('shopPage',infomsg="Payment for #" + id + " Successful."))
            else:
                return redirect(url_for('shopPage', infomsg="You already purchased this item. You cannot purchase it once again."))
        else:
            return redirect(url_for('shopPage', infomsg="Insufficient Balance!"))

    @app.route("/todo")
    @login_required
    def todoList():
        currentUserID = current_user.id
        infomsg = request.args.get("infomsg","")
        coins = getCoins(currentUserID)
        result = Todo.query.join(Todo, Requests.requestID == Todo.requestID). \
                add_columns(Todo.todoID, Todo.requestID, Requests.title, Todo.status). \
                filter(Todo.userID == currentUserID).all()
            # Fetch TodoID, requestID, Request Title, Request Status by inner join
        if result:
            return render_template("todo.html", result=result, coins=coins, infomsg=infomsg)
        else:
            return render_template("todo.html", errmsg=f"We cannot find any content.", coins=coins)
        
    @app.route("/leaderboard")
    @login_required
    def leaderBoard():
        currentUserID = current_user.id
        requestCount, todoCount = getCountForLeaderboard() 
            # Count Request Count and Todo Count for each user in DB and get the return subquery objects
        result = db.session.query(UserInfo). \
                    outerjoin(requestCount, UserInfo.userID == requestCount.c.userID). \
                    outerjoin(todoCount, UserInfo.userID == todoCount.c.userID). \
                    add_columns(UserInfo.userID, UserInfo.coins, 
                                func.coalesce(requestCount.c.requestcount, 0).label("requestcount"),
                                func.coalesce(todoCount.c.todocount, 0).label("todoidcount")). \
                    group_by(UserInfo.userID). \
                    order_by(UserInfo.coins.desc()).all()
        # requestCount.c.userID = read userID from subquery object named requestCount
        # todoCount.c.userID = read userID from subquery object named todoCount
        # func.coalesce = count of requests and todo, if no request posted, 
        # mark as 0. And label these columns as requestcount and todoidcount,
        # and group by the userID to avoid from duplicate count
        # Ranking user based on coin amounts in decreasing sort. Get all results.
        if result:
            return render_template("leaderboard.html", result=result, curusrid=currentUserID)
        else:
            return render_template("leaderboard.html", errmsg=f"We cannot find any content.")
        
    @app.route("/api/searchuser/<type>/<value>",methods=["GET"])
    @login_required
    def searchFriend(type,value):
        if type == "country":
            result = UserInfo.query.filter(UserInfo.country.ilike('%' + value + '%')).all()
        elif type == "email":
            result = UserInfo.query.filter(UserInfo.email.ilike('%' + value + '%')).all()
        else:
            return jsonify([])
        if result:
            user_data = [{'id': user.userID, 'email': user.email, 'country': user.country} for user in
                         result]
        else:
            user_data = []
        return jsonify(user_data)
    
    @app.route("/robots.txt") # Discourage search engine to index this website
    def robots():
        return render_template("robots.txt")

# APIs for LLM auto generate & filled, which called by Javascript

    @app.route("/api/llmrequest")
    def llmreq():
        return llm.llmRequests()
    
    @app.route("/api/llmanswer")
    def llmans():
        return llm.llmAnswers()
    
    @app.route("/api/feelingsllm")
    def llmfeel():
        return llm.llmFeelings()

except Exception as e:
    print("Error occured. Cannot proceed. Exiting system...")
    print("Details: " + str(e))
    exit(-1)
# If file is missing, the program cannot start

if __name__ == "__main__":
    app.run()
