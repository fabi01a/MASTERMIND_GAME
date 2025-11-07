from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.routes import routes

#create db instance globally
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    
    #configure SQLite as the DB
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mastermind.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #initialize extentions
    db.init_app(app)
    migrate.init_app(app, db)

    #import models so Flask-Migrate can see them
    from app.models.player import Player
    from app.models.gameSession  import GameSession
    from app.models.guess import Guess
    
    #import and register routes
    from app.routes import routes
    app.register_blueprint(routes)
    
    return app