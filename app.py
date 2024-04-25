import os
from flask import *
import apps.llm as llm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from apps.login_process import login_required
from models.sqlmodels import *
from models.formModels import *
from apps.get import *
from apps.login_process import *
from apps.randomprofile import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'database', 'main.db')
app.config['SECRET_KEY'] = randomSessionKey(16) # Secret Key for all sessions
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
connect = engine.connect()
alchemySession = sessionmaker(bind=engine)

dbSession = alchemySession()
db.init_app(app) # Create a new instance. db has been defined in sqlmodel.py
migrate = Migrate(app, db) # Create a flask db migration

try:
    @app.route("/")
    def homepage():
        return render_template('index.html')

    @app.route("/login", methods=["GET"])
    def loginPage():
        form = LoginForm()
        if request.method == "GET":
            errormsg = request.args.get('errormsg', '')
            return render_template('login.html', errormsg=errormsg, form=form)
        else:
            return render_template('login.html',form=form)

    @app.route("/register", methods=["GET", "POST"])
    def registerPage():
        form = RegisterForm()
        if request.method == "POST":
            userID = str(uuidGen())
            email = form.email.data
            password = form.password.data
            country = str(rp.randomCountry())
            pincode = form.pin_code.data
            try:
                checkEmailExist = checkEmail(email)
                if checkEmailExist == 0:
                    encryptedPassword = encryptPassword(password)
                    insert = UserInfo(userID=userID,email=email,password=encryptedPassword,country=country,pincode=pincode)
                    dbSession.add(insert)
                    dbSession.commit()
                    return render_template("register_complete.html")
                else:
                    return redirect(url_for('registerPage', errormsg="Email already exists"))
            except Exception as e:
                print(e)
                return redirect(url_for('registerPage', errormsg="An error occurred"))
        else:
            errormsg = request.args.get('errormsg', '')
            return render_template('register.html', errormsg=errormsg, form=form)
        
    @app.route("/forgetpassword", methods=["GET","POST"])
    def forgetPassword():
        form = ForgetPasswordForm()
        if request.method == "POST":
            email = form.email.data
            pincode = form.pin_code.data
            fetchEmail = checkEmail(email)
            if fetchEmail == -1:
                pin_verify_result = verifyPinCode(email, pincode)
                if pin_verify_result == 0:
                    try:
                        encryptedPassword = encryptPassword("123")
                        dbSession.execute(update(UserInfo).filter(UserInfo.email == email).values(password=encryptedPassword))
                        dbSession.commit()
                        return "<script>alert('Your password has been reset to: 123.');window.location.href='/login';</script>"
                    except Exception as e:
                        print(f"Error resetting password: {str(e)}")
                        return redirect(url_for('forgetPassword', infomsg="Failed to reset password. Please contact support."))
                else:
                    return redirect(url_for('forgetPassword', infomsg="Incorrect PIN."))
            else:
                return redirect(url_for('forgetPassword', infomsg="User not found."))
        else:
            errormsg = request.args.get("infomsg","")
            return render_template('forget_password.html', errormsg=errormsg, form=form)
    
    @app.route("/modifycenter",methods=["GET","POST"])
    @login_required
    def modifyCentre():
        if request.method == "POST":
            userID = getSession("userid")
            changeType = request.form["type"]
            if changeType == "email":
                newemail = request.form["newEmail"]
                dbSession.execute(update(UserInfo).where(UserInfo.userID==userID).values(email=newemail))
            elif changeType == "country":
                country = request.form["country"]
                dbSession.execute(update(UserInfo).where(UserInfo.userID==userID).values(country=country))
            elif changeType == "pin":
                newpin = request.form["newpin"]
                dbSession.execute(update(UserInfo).where(UserInfo.userID==userID).values(pincode=newpin))
            elif changeType == "password":
                newpassword = request.form["newpassword"]
                encNewPassword = encryptPassword(newpassword)
                dbSession.execute(update(UserInfo).where(UserInfo.userID==userID).values(password=encNewPassword))
            else:
                return render_template("change_profile.html",infomsg="Invalid Change!")
            dbSession.commit()
            return redirect(url_for("profilePage",infomsg="Information " + changeType + " has been updated."))
        else:
            return render_template("change_profile.html")

    @app.route("/community", methods=["GET"])
    @login_required
    def communityPage():
        userID = getSession("userid")
        try:
            result = Community.query.all()
            return render_template('community.html', result=result, userID=userID)
        except Exception as e:
            print(e)
            return render_template('community.html', errmsg="Internal Error")
        
    @app.route("/chat")
    @login_required
    def chatPage():
        userID = getSession("userid")
        infomsg = request.args.get("infomsg","")
        result = Chats.query.filter(or_(Chats.dstUserID == userID, Chats.srcUserID == userID)).all()
        if result:
            return render_template('chat.html', results=result, infomsg=infomsg)
        else:
            return render_template('chat.html', infomsg="No chat. Do you want to set up a new one?")
    
    @app.route("/chat/<chatid>")
    @login_required
    def chatDetailsPage(chatid):
        dstuser = getChatInfo(chatid,"dstuser")
        result = Chats.query.filter(Chats.chatID == chatid).all()
        if result:
            return render_template('chat_details.html',results=result, dstUser=dstuser, chatID=chatid)
        else:
            return render_template('chat_details.html', infomsg="Unexpected error")
        
    @app.route("/dochatreply",methods=['GET','POST'])
    @login_required
    def doChatReply():
        if request.method == "POST":
            userID = getSession("userid")
            chatID = request.form['chatID']
            content = request.form['content']
            dstuser = request.form['dstUser']
            try:
                insert = Chats(chatID=chatID,srcUserID=userID,dstUserID=dstuser,content=content)
                dbSession.add(insert)
                dbSession.commit()
                return "<script>alert('Message sent.');window.location.href='/chat/" + chatID + "';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('chatPage', errmsg="Internal Error"))
        else:
            return redirect(url_for('chatPage', errmsg="Invalid Request!"))
        
    @app.route("/deletechat/<chatid>", methods=['GET'])
    @login_required
    def deleteChat(chatid):
        currentuserID = getSession("userid")
        dstuser = getChatInfo(chatid,"dstuser")
        srcuser = getChatInfo(chatid,"srcuser")
        if int(dstuser) == int(currentuserID) or int(srcuser) == int(currentuserID): # Only userID matches can delete
            dbSession.execute(delete(Chats).where(Chats.chatID == chatid))
            dbSession.commit()
            return "<script>alert('Your chat has been deleted.');window.location.href='/chat';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/chat';</script>"

    @app.route("/deletethread/<threaduserid>/<threadID>", methods=['GET'])
    @login_required
    def deleteThread(threaduserid,threadID):
        currentuserID = getSession("userid")
        if int(threaduserid) == int(currentuserID): # Only userID matches can delete
            dbSession.execute(delete(Thread).where(Thread.threadID == threadID))
            dbSession.execute(delete(Community).where(Community.threadID == threadID))
            dbSession.commit()
            return "<script>alert('Your thread has been deleted.');window.location.href='/community';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/community';</script>"
        
    @app.route("/newchat",methods=['GET','POST'])
    @login_required
    def donewchat():
        form = newChatForm()
        if request.method == "POST":
            chatUUID = str(uuidGen())
            userID = getSession("userid")
            dstuser = form.dstUser.data
            content = form.contents.data
            try:
                insert = Chats(chatID=chatUUID,srcUserID=userID,dstUserID=dstuser,content=content)
                dbSession.add(insert)
                dbSession.commit()
                return "<script>alert('New ticket recorded.');window.location.href='/chat';</script>"
            except Exception as e:
                print(e)
                return redirect(url_for('chatPage', errmsg="Internal Error"))
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
            currentUserID = getSession("userid")
            coins = getCoins(currentUserID)
            result = Requests.query.all()
            return render_template('requests.html', result=result, coins=coins, userid=currentUserID)
        except Exception as e:
            print(e)
            return render_template('requests.html', errmsg="Internal Error")

    @app.route("/shop",methods=["GET"])
    @login_required
    def shopPage():
        userID = getSession("userid")
        currentCoin = getCoins(userID)
        infomsg = request.args.get("infomsg","")
        result = Shop.query.all()
        if result:
            return render_template('shop.html',coins=currentCoin,results=result, infomsg=infomsg)
        else:
            return render_template('shop.html', coins=currentCoin, infomsg="Unexpected error")
    
    @app.route("/signs",methods=["POST","GET"])
    @login_required
    def signPage():
        form = signEmotionForm()
        signSessionID = uuidGen()
        userID = getSession("userid")
        timeObject = datetime.now()
        currentDay = str(timeObject.year) + "/" + str(timeObject.month) + "/" + str(timeObject.day)
        currentCoin = getCoins(userID)
        infomsg = request.args.get("infomsg","")
        ifSigned = ifSign(userID)
        if request.method == "POST":
            feelings = form.feelings.data
            comments = form.comments.data
            if not ifSigned:
                try:
                    randomRewards = int(randomCoinRewards())
                    rewardCoins = randomRewards + int(currentCoin)
                    insert = Signs(signID=signSessionID,userID=userID,time=currentDay,emotion=feelings,comments=comments,rewards=randomRewards)
                    dbSession.add(insert)
                    dbSession.execute(update(UserInfo).where(UserInfo.userID==userID).values(coins=rewardCoins))
                    dbSession.commit()
                    return redirect(url_for('profilePage',infomsg="Signed successfully! Welcome back and you have get " 
                                            + str(randomRewards) + " coins for reward!"))
                except Exception as e:
                    print("[ERROR] SignPage: " + str(e))
                    return render_template('signs.html',infomsg="Internal Error! <a href='/profile' title='Profile'>Click here for your profile</a>",
                                           form=form)
            else:
                return render_template('signs.html',infomsg="You have signed today! <a href='/profile' title='Profile'>Click here for your profile</a>",
                                       form=form)
        else:
            return render_template('signs.html',infomsg=infomsg,form=form)

    @app.route("/newthread",methods=["GET","POST"])
    @login_required
    def newThread():
        form = newThreadForm()
        if request.method == "POST":
            userID = getSession("userid")
            title = form.title.data
            content = form.contents.data
            try:
                threadUUID = str(uuidGen())
                inserts = [Community(threadID=threadUUID,title=title,userID=userID),
                           Thread(threadID=threadUUID,userID=userID,contents=content)]
                for item in inserts:
                    dbSession.add(item)
                dbSession.commit()
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
        if request.method == "POST":
            userID = getSession("userid")
            currentCoins = getCoins(userID)
            title = form.title.data
            content = form.contents.data
            rewards = form.rewards.data
            timelimit = form.timelimit.data
            if int(rewards) <= int(currentCoins):
                insert = Requests(title=title,content=content,rewards=rewards,timelimit=timelimit,userID=userID)
                remainCoins = int(currentCoins) - int(rewards)
                coins = update(UserInfo).filter(UserInfo.userID == userID).values(coins=remainCoins)
                dbSession.add(insert)
                dbSession.execute(coins)
                dbSession.commit()
                return "<script>alert('New request posted.');window.location.href='/requests';</script>"
            else:
                return redirect(url_for('newRequest', msg="Insufficient Balance!"))
        else:
            msg = request.args.get('msg', '')
            userID = getSession("userid")
            currentCoin = getCoins(userID)
            return render_template('newrequest.html', balance=currentCoin,msg=msg,form=form)
    
    @app.route("/logout")
    @login_required
    def logoutPage():
        destroySession()
        response = make_response(render_template('logout.html'))
        response.set_cookie('session','',expires=0)
        return response

    @app.route("/donewthreadreply", methods=['GET', 'POST'])
    @login_required
    def doNewThreadReply():
        if request.method == "POST":
            userID = getSession("userid")
            content = request.form['content']
            threadUUID = request.form['threadID']
            try:
                insert = Thread(threadID=threadUUID,userID=userID,contents=content)
                dbSession.add(insert)
                dbSession.commit()
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
            encryptedPassword = encryptPassword(password)
            result = UserInfo.query.filter(UserInfo.email == email, UserInfo.password == encryptedPassword).first()
            if result:
                userid = str(result.userID)
                print("[Info] User " + userid + " has login in.")
                setSession(userid,email)
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
            keyword = request.form['keyword'].strip()  # assuming the form field is named 'keyword'
            result = Community.query.filter(or_(Community.threadID.ilike('%' + keyword + '%'), 
                        Community.title.ilike('%' + keyword + '%')))
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
            result = Requests.query.filter(or_(Requests.requestID.ilike('%' + keyword + '%'), 
                        Requests.title.ilike('%' + keyword + '%')))
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
            keyword = request.form['keyword'].strip()  # assuming the form field is named 'keyword'
            result = Chats.query.filter(or_(Chats.srcUserID.ilike('%' + keyword + '%'), 
                        Chats.dstUserID.ilike('%' + keyword + '%')))
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
            userID = getSession("userid")
            pincode = getUserInfo(userID, "pincode")
            user_details = UserInfo.query.filter(UserInfo.userID == userID).all()  # User Info
            if user_details is None:
                return render_template('profile.html', errmsg="User not found")
            nft_details = Transaction.query.filter(Transaction.userID==userID).all()
            signHistory = Signs.query.filter(Signs.userID == userID).all()
            nftid = str(getUserInfo(userID, "avatar"))  # Get avatar ID
            return render_template('profile.html',
                                userID=userID,
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
        
    @app.route('/profile/<userid>')
    @login_required
    def profilePageOthersView(userid):
        try:
            infomsg = request.args.get('infomsg', '')
            userID = userid
            user_details = UserInfo.query.filter(UserInfo.userID == userID).all()
            if user_details is None:
                return "<script>alert('Cannot find this user');history.back();</script>"
            avatar_id = str(getUserInfo(userID,"avatar"))
            return render_template('profile_other_user_view.html',
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
        userID = getSession("userid")
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
        for item in updates:
            dbSession.execute(item)
        dbSession.commit()
        return redirect(url_for('todoList',infomsg="Thank you! You have completed the request."))
    
    @app.route("/thread/<id>", methods=['GET'])
    @login_required
    def threadDetails(id):
        thread_title = getThreadTitle(id)
        result = Thread.query.filter(Thread.threadID == id).all()
        if result:
            return render_template("thread_details.html", result=result, threadID=id, threadName=thread_title)
        else:
            return render_template("thread_details.html", errmsg=f"We cannot find any content.")
    
    @app.route("/acceptrequest/<id>", methods=['GET'])
    @login_required
    def acceptRequest(id):
        result = Requests.query.filter(Requests.requestID == id).first()
        if result:
            return render_template("accept_request.html", result=result)
        else:
            return render_template("accept_request.html", errmsg=f"We cannot find any content.")   
        
    @app.route("/confirmpayment/<id>", methods=['GET'])
    @login_required
    def confirmPayment(id):
        result = Shop.query.filter(Shop.itemID == id).first()
        if result:
            return render_template("confirm_buy.html", result=result)
        else:
            return render_template("confirm_buy.html", errmsg=f"We cannot find any content.")   

    @app.route("/deleterequest/<userid>/<requestid>", methods=['GET'])
    @login_required
    def deleteRequest(userid,requestid):
        currentuserID = getSession("userid")
        state = getRequestInfo(requestid,"state")
        currentCoins = getUserInfo(userid,"coins")
        currentReqRewards = getRequestInfo(requestid,"rewards")
        remainCoins = int(currentCoins) + int(currentReqRewards) # Refund coins
        if int(userid) == int(currentuserID) and state == "Available": # Only userID matches and status is Available can delete
            commands = [delete(Requests).where(Requests.requestID == requestid),
                        update(UserInfo).filter(UserInfo.userID == userid).values(coins=remainCoins)]
            for item in commands:
                dbSession.execute(item)
            dbSession.commit()
            return "<script>alert('Request Deleted Successfully. Your reward has been refunded.');window.location.href='/requests';</script>"
        else:
            return "<script>alert('You cannot delete it!');window.location.href='/requests';</script>"

    @app.route("/myrequest")
    @login_required
    def myRequest():
        userID = getSession("userid")
        result = Requests.query.filter(Requests.userID == userID)
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
        userID = getSession("userid")
        updateReq = update(Requests).where(Requests.requestID == id).values(status="accepted")
        insertTodo = Todo(userID=userID,requestID=id,status="Accepted")
        dbSession.execute(updateReq)
        dbSession.add(insertTodo)
        dbSession.commit()
        return redirect(url_for('todoList'))

    @app.route("/setavatar/<id>", methods=['GET'])
    @login_required
    def doSetAvatar(id):
        userID = getSession("userid")
        updateusr = update(UserInfo).where(UserInfo.userID == userID).values(avatar=id)
        dbSession.execute(updateusr)
        dbSession.commit()
        return redirect(url_for('profilePage',infomsg="Avatar updated."))
    
    @app.route("/dopayment/<id>", methods=['GET'])
    @login_required
    def doPayment(id):
        userID = getSession("userid")
        itemPrice = getItemInfo(id,"price")
        userCoins = getUserInfo(userID,"coins")
        remainCoins = int(userCoins) - int(itemPrice)
        checkWarehouse = ifUserPurchased(userID,id) # Check if user already purchased this item
        if remainCoins >= 0:
            if not checkWarehouse:
                insert = Transaction(userID=userID,itemID=id)
                dbSession.add(insert)
                dbSession.execute(update(UserInfo).filter(UserInfo.userID == userID).values(coins=remainCoins))
                dbSession.commit()
                return redirect(url_for('shopPage',infomsg="Payment for #" + id + " Successful."))
            else:
                return redirect(url_for('shopPage', infomsg="You already purchased this item. You cannot purchase it once again."))
        else:
            return redirect(url_for('shopPage', infomsg="Insufficient Balance!"))

    @app.route("/todo")
    @login_required
    def todoList():
        currentUserID = getSession("userid")
        infomsg = request.args.get("infomsg","")
        coins = getCoins(currentUserID)
        result = Todo.query.filter(Todo.userID == currentUserID)
        if result:
            return render_template("todo.html", result=result, coins=coins, infomsg=infomsg)
        else:
            return render_template("todo.html", errmsg=f"We cannot find any content.", coins=coins)
        
    @app.route("/leaderboard")
    @login_required
    def leaderBoard():
        result = UserInfo.query.order_by(UserInfo.coins.desc())
        if result:
            return render_template("leaderboard.html", result=result)
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
    
    @app.route("/robots.txt")
    def robots():
        return render_template("robots.txt")

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
