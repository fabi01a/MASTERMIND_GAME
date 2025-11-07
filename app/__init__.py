import os
from flask import Flask
from app.extensions import db, migrate

def create_app(test_config=None):
    app = Flask(__name__)
    
    #configure SQLite as the DB
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'mastermind.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #initialize extentions
    db.init_app(app)
    migrate.init_app(app, db)

    #import and register routes
    from app.routes import routes
    app.register_blueprint(routes)

    #import models so Flask-Migrate can see them
    from app.models.player import Player
    from app.models.gameSession  import GameSession
    from app.models.guess import Guess
    

    return app