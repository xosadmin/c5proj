import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import mainBluePrint, login_manager
from models.sqlmodels import db
from apps.get import randomSessionKey

# Initialize Flask app and database migration
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = randomSessionKey(16)  # Secret Key for all sessions
    
    if config is not None:
        app.config.update(config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.getcwd(), 'database', 'main.db')
    
    # Register Blueprints
    app.register_blueprint(mainBluePrint)
    
    # Initialize database and login manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "mainBluePrint.loginPage"  # Default Login View
    
    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run()

