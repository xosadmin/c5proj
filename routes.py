from flask import *
import apps.llm as llm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from models.sqlmodels import *
from models.formModels import *
from models.loginModels import *
from apps.get import *
from apps.randomprofile import *
from flask import Blueprint

login_manager = LoginManager()
mainBluePrint = Blueprint('mainBluePrint', __name__)

try:
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @mainBluePrint.route("/index")
    @mainBluePrint.route("/")
    def homepage():
        if current_user.is_authenticated:
            return redirect(url_for('mainBluePrint.profilePage',infomsg="You have already logged in. Welcome Back!"))
        else:
            return render_template('index.html')

    @mainBluePrint.route("/login", methods=["GET"])
    def loginPage():
        form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('mainBluePrint.profilePage',infomsg="You have already logged in. Welcome Back!"))
        else:
            errormsg = request.args.get('errormsg', '')
            return render_template('login.html', errormsg=errormsg, form=form)

    @mainBluePrint.route("/register", methods=["GET", "POST"])
    def registerPage():
        form = RegisterForm()
        if current_user.is_authenticated:
            return redirect(url_for('mainBluePrint.profilePage',infomsg="You have already logged in. Welcome Back!"))
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
                        return redirect(url_for('mainBluePrint.registerPage', errormsg="Email already exists or password mismatch"))
                except Exception as e:
                    print(e)
                    return redirect(url_for('mainBluePrint.registerPage', errormsg="An error occurred"))
            else:
                errormsg = request.args.get('errormsg', '')
                return render_template('register.html', errormsg=errormsg, form=form)
        
    @mainBluePrint.route("/forgetpassword", methods=["GET","POST"])
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
                            return redirect(url_for('mainBluePrint.forgetPassword', infomsg="Failed to reset password due to system error."))
                    else: # If it's not incorrect
                        return redirect(url_for('mainBluePrint.forgetPassword', infomsg="Incorrect PIN."))
                else: # If the backend cannot find the user
                    return redirect(url_for('mainBluePrint.forgetPassword', infomsg="User not found."))
            else:
                infomsg = request.args.get('infomsg','')
                return render_template('forget_password.html', errormsg=infomsg, form=form)
        else:
            errormsg = "You cannot perform this request while signed in."
            return redirect(url_for('mainBluePrint.profilePage', infomsg=errormsg))
            # If user is logged in, this function is disabled until logout

    @mainBluePrint.route("/signs",methods=["POST","GET"])
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
                    return redirect(url_for('mainBluePrint.profilePage',infomsg="Signed successfully! Welcome back and you have get " 
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
    
    @mainBluePrint.route("/modifycenter",methods=["GET","POST"])
    @login_required
    def modifyCentre():
        if request.method == "POST": # If user triggered submit button
            userID = current_user.id # Fetch current logged in user ID
            changeType = request.form["type"]
            if changeType == "email":
                newEmail = request.form["newEmail"]
                verifyEmailResult = checkEmail(newEmail) # Verify provided new email existing in the system
                if verifyEmailResult == -1: # If exists.
                    return render_template("change_profile.html",infomsg="Email address already exists!")                    
                else: # If new email not exists in the system
                    db.session.execute(update(UserInfo).where(UserInfo.userID==userID).values(email=newEmail))                                    
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
            return redirect(url_for("mainBluePrint.profilePage",infomsg=changeType + " has been updated."))
        else:
            return render_template("change_profile.html")

    @mainBluePrint.route("/community", methods=["GET"])
    @login_required
    def communityPage():
        userID = current_user.id # Fetch current logged in user ID
        try:
            result = Community.query.all() # Fetch all data from Community
            return render_template('community.html', result=result, userID=userID)
        except Exception as e:
            print(e) # Print error in the console
            return render_template('community.html', errmsg="Internal Error")
        
    @mainBluePrint.route("/chat")
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

    @mainBluePrint.route("/chat/<chatid>")
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
        
    @mainBluePrint.route("/dochatreply",methods=['GET','POST'])
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
                return "<script>window.location.href='/chat/" + chatID + "';</script>"
                # Prompt dialog to notify Message sent to user
            except Exception as e:
                print(e) # Print detailed error on the console
                return redirect(url_for('mainBluePrint.chatPage', errmsg="Internal Error"))
        else:
            return redirect(url_for('mainBluePrint.chatPage', errmsg="Invalid Request!"))
        
    @mainBluePrint.route("/deletechat/<chatid>", methods=['GET'])
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

    @mainBluePrint.route("/deletethread/<threaduserid>/<threadID>", methods=['GET'])
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
        
    @mainBluePrint.route("/newchat",methods=['GET','POST'])
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
                    return redirect(url_for('mainBluePrint.chatPage', errmsg="Internal Error"))
            else:
                return render_template("newchat.html", form=form, infomsg="Destination user not exists or you cannot send ticket to yourself!")
        else:
            return render_template("newchat.html", form=form)

    @mainBluePrint.route("/newchat/<dstuserid>", methods=['GET'])
    @login_required
    def donewchatwithID(dstuserid):
        form = newChatForm()
        return render_template("newchat.html", dstuserid=dstuserid, form=form)

    @mainBluePrint.route("/requests",methods=["GET"])
    @login_required
    def requestPage():
        try:
            currentUserID = current_user.id
            coins = getCoins(currentUserID)
            infomsg = request.args.get("infomsg","")
            result = Requests.query.filter(Requests.status == "Available").all() # Fetch all available requests from DB
            return render_template('requests.html', result=result, coins=coins, userid=currentUserID,infomsg=infomsg)
        except Exception as e:
            print(e) # Print detailed error on the console
            return render_template('requests.html', errmsg="Internal Error")

    @mainBluePrint.route("/shop",methods=["GET"])
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

    @mainBluePrint.route("/newthread",methods=["GET","POST"])
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
                return redirect(url_for('mainBluePrint.newThread', errmsg="Internal Error"))
        else:
            return render_template('newthread.html',form=form)
    
    @mainBluePrint.route("/newrequest",methods=["GET","POST"])
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
                return redirect(url_for('mainBluePrint.newRequest', msg="Insufficient Balance!"))
        else:
            msg = request.args.get('msg', '')
            userID = current_user.id
            currentCoin = getCoins(userID)
            return render_template('newrequest.html', balance=currentCoin,msg=msg,form=form)
    
    @mainBluePrint.route("/logout")
    @login_required
    def logoutPage():
        logout_user() # Logout user and destroy session
        return render_template('logout.html')

    @mainBluePrint.route("/donewthreadreply", methods=['GET', 'POST'])
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
                return "<script>window.location.href='/thread/"+ threadUUID +"';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('mainBluePrint.newThread', errmsg="Internal Error"))
        else:
            return redirect(url_for('mainBluePrint.newThread', errmsg="Invalid Request!"))

    @mainBluePrint.route("/dologin",methods=['GET','POST'])
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
                    return redirect(url_for('mainBluePrint.profilePage', userid=userid, infomsg="Welcome back to Adventurers Guild!")) # If username and password is correct
                else:
                    return redirect(url_for('mainBluePrint.signPage'))
            else:
                return redirect(url_for('mainBluePrint.loginPage', errormsg="Wrong email/password input!"))
        else:
            return redirect(url_for('mainBluePrint.loginPage', errormsg="Invalid Request!")) # If the user attempts to use GET method to pass the data
        
    @mainBluePrint.route("/docommsearch", methods=['GET', 'POST'])
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
        
    @mainBluePrint.route("/doreqsearch", methods=['GET', 'POST'])
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
        
    @mainBluePrint.route("/dochatsearch", methods=['GET', 'POST'])
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
    
    @mainBluePrint.route('/profile')
    @login_required
    def profilePage():
        try:
            infomsg = request.args.get('infomsg', '')
            userID = current_user.id
            pincode = getUserInfo(userID, "pincode")
            user_details = UserInfo.query.filter(UserInfo.userID == userID).all()  # User Info
            if user_details is None:
                return render_template('profile.html', errmsg="User not found")
            nft_details = Transaction.query.join(Transaction, Transaction.itemID == Shop.itemID). \
                        add_columns(Transaction.transactionID, Shop.itemID, Shop.itemDetail). \
                        filter(Transaction.userID==userID).all()
            signHistory = Signs.query.filter(Signs.userID == userID).limit(5).all()
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
        
    @mainBluePrint.route('/profile/<userid>') # User profile in 3rd user view
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

    @mainBluePrint.route('/answerrequest/<requestid>')
    @login_required
    def answerRequest(requestid):
        userID = current_user.id
        result = Requests.query.filter(Requests.requestID == requestid).first()
        if result:
            return render_template("answerrequest.html", result=result, userID=userID)
        else:
            return render_template("answerrequest.html", errmsg=f"We cannot find any content.")

    @mainBluePrint.route("/doanswerrequest", methods=['POST'])
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
        return redirect(url_for('mainBluePrint.todoList',infomsg="Thank you! You have completed the request."))

    @mainBluePrint.route("/thread/<id>", methods=['GET'])
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
    
    @mainBluePrint.route("/acceptrequest/<id>", methods=['GET'])
    @login_required
    def acceptRequest(id):
        result = Requests.query.filter(Requests.requestID == id).first() # Get the request details
        if result:
            return render_template("accept_request.html", result=result)
        else:
            return render_template("accept_request.html", errmsg=f"We cannot find any content.")   
        
    @mainBluePrint.route("/confirmpayment/<id>", methods=['GET'])
    @login_required
    def confirmPayment(id):
        result = Shop.query.filter(Shop.itemID == id).first() # Get the item details
        if result:
            return render_template("confirm_buy.html", result=result)
        else:
            return render_template("confirm_buy.html", errmsg=f"We cannot find any content.")   

    @mainBluePrint.route("/deleterequest/<userid>/<requestid>", methods=['GET'])
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

    @mainBluePrint.route("/myrequest")
    @login_required
    def myRequest():
        userID = current_user.id
        result = Requests.query.filter(Requests.userID == userID).all() # Show all requests that current user posted
        if result:
            return render_template("myrequest.html", result=result)
        else:
            return render_template("myrequest.html", errmsg=f"We cannot find any content.")

    @mainBluePrint.route("/requestdetails/<id>", methods=['GET'])
    @login_required
    def requestDetails(id):
        result = Requests.query.filter(Requests.requestID == id).first()
        if result:
            return render_template("requestDetail.html", result=result)
        else:
            return render_template("requestDetail.html", errmsg=f"We cannot find any content.")
        
    @mainBluePrint.route("/doacceptrequest/<id>", methods=['GET'])
    @login_required
    def doAcceptRequest(id):
        userID = current_user.id
        requestBelongs = getRequestInfo(id,"userID")
        if userID != requestBelongs:
            updateReq = update(Requests).where(Requests.requestID == id).values(status="accepted") # Change the request state to accepted
            insertTodo = Todo(userID=userID,requestID=id,status="Accepted") # Update this request to user's todo list
            db.session.execute(updateReq)
            db.session.add(insertTodo)
            db.session.commit()
            return redirect(url_for('mainBluePrint.todoList'))
        else:
            return "<script>alert('You cannot accept your own request.');window.location.href='/requests';</script>"

    @mainBluePrint.route("/setavatar/<id>", methods=['GET'])
    @login_required
    def doSetAvatar(id):
        userID = current_user.id
        updateusr = update(UserInfo).where(UserInfo.userID == userID).values(avatar=id) # Set the avatar with specific ID for current user
        db.session.execute(updateusr)
        db.session.commit()
        return redirect(url_for('mainBluePrint.profilePage',infomsg="Avatar updated."))
    
    @mainBluePrint.route("/dopayment/<id>", methods=['GET'])
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
                return redirect(url_for('mainBluePrint.shopPage',infomsg="Payment for #" + id + " Successful."))
            else:
                return redirect(url_for('mainBluePrint.shopPage', infomsg="You already purchased this item. You cannot purchase it once again."))
        else:
            return redirect(url_for('mainBluePrint.shopPage', infomsg="Insufficient Balance!"))

    @mainBluePrint.route("/todo")
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
        
    @mainBluePrint.route("/leaderboard")
    @login_required
    def leaderBoard():
        currentUserID = current_user.id
        requestCount, todoCount = getCountForLeaderboard() 
            # Count Request Count and Todo Count for each user in DB and get the return subquery objects
        result = db.session.query(UserInfo). \
                    outerjoin(requestCount, UserInfo.userID == requestCount.c.userID). \
                    outerjoin(todoCount, UserInfo.userID == todoCount.c.userID). \
                    add_columns(UserInfo.userID, UserInfo.coins, UserInfo.country,
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
        
    @mainBluePrint.route("/help",methods=["GET","POST"])
    @login_required
    def helpCenter():
        currentUserID = current_user.id
        showTranscription = FaqChatTransaction.query.filter(FaqChatTransaction.userID == currentUserID).all()
        if request.method == "POST":
            userInput = request.form["content"]
            userInputStore = FaqChatTransaction(userID=currentUserID,role="User",content=userInput)
            userInputSplit = str(userInput).lower().split(" ")
            for item in userInputSplit:
                result = Faq.query.filter(or_(Faq.keyword.ilike(f'%{item}%'), Faq.answer.ilike(f'%{item}%'))).first()
                # Look up answer from both keyword and answer columns
                if result:
                    newResult = FaqChatTransaction(userID=currentUserID,role="Help Bot", content=result.answer)
                    #break
                else:
                    newResult = FaqChatTransaction(userID=currentUserID,role="Help Bot", content="I can't find any answer.")
            db.session.add(userInputStore)
            db.session.add(newResult)
            db.session.commit()
            return redirect(url_for("mainBluePrint.helpCenter"))
        else:
            return render_template("helpcenter.html",showTranscription=showTranscription)
    
    @mainBluePrint.route("/clearhelp")
    @login_required
    def ClearHelpCenter():
        currentUserID = current_user.id
        db.session.execute(delete(FaqChatTransaction).where(FaqChatTransaction.userID == currentUserID))
        db.session.commit()
        return "<script>alert('You have started a new help session.');window.location.href='/help';</script>"
        
    @mainBluePrint.route("/api/searchuser/<type>/<value>",methods=["GET"])
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
    
    @mainBluePrint.route("/robots.txt") # Discourage search engine to index this website
    def robots():
        return render_template("robots.txt")

# APIs for LLM auto generate & filled, which called by Javascript

    @mainBluePrint.route("/api/llmrequest")
    def llmreq():
        return llm.llmRequests()
    
    @mainBluePrint.route("/api/llmanswer")
    def llmans():
        return llm.llmAnswers()
    
    @mainBluePrint.route("/api/feelingsllm")
    def llmfeel():
        return llm.llmFeelings()

except Exception as e:
    print("Error occured. Cannot proceed. Exiting system...")
    print("Details: " + str(e))
    exit(-1)
# If file is missing, the program cannot start
