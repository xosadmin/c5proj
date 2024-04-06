from flask import *
from sqlite import *
import sqlite3
import llm
import randomprofile as rp

app = Flask(__name__)

try:
    @app.route("/")
    def homepage():
        return render_template('index.html')

    @app.route("/login")
    def loginPage():
        return render_template('login.html')

    @app.route("/register")
    def registerPage():
        return render_template('register.html')

    @app.route("/community")
    def communityPage():
        return render_template('community.html')
    
    @app.route("/requests")
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
    
    @app.route('/profile')
    def profilePage():
        return render_template('profile.html',
                               username='example_user',
                               email='1@1.com',
                               nickname=rp.randomNickname(),
                               location=rp.randomCountry(),
                               coins='0',
                               nftid='1',
                               nftname='test',
                               RewardID='1',
                               RewardName='test'
                               )
    
    @app.route("/rewards/<username>")
    def rewardPage():
        return render_template('rewards.html', username='username')
    
    @app.route("/llmrequest")
    def llmreq():
        return llm.llmRequests()
    
    @app.route("/llmanswer")
    def llmans():
        return llm.llmAnswers()

except:
    print("File missing. Cannot proceed. Exiting system...")
    exit(-1)
# If file is missing, the program cannot start

if __name__ == "__main__":
    app.run()
