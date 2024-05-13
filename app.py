import os
from flask import *
import apps.llm as llm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import mainBluePrint,login_manager
from models.sqlmodels import *
from models.formModels import *
from models.loginModels import *
from apps.get import *
from apps.randomprofile import *

#app = Flask(__name__)
migrate = Migrate(app, db) # Create a flask db migration

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = randomSessionKey(16) # Secret Key for all sessions
    if config is not None:
        app.config.update(config)
    else: 
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'database', 'main.db')
    app.register_blueprint(mainBluePrint)
    db.init_app(app) # Create a new instance. db has been defined in sqlmodel.py
    login_manager.init_app(app) # Create a new Login manager
    login_manager.login_view = "mainBluePrint.loginPage" # Default Login View
    return app

app = create_app()

if __name__ == "__main__":
    app.run()
