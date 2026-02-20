# review
import os
from flask import Flask
from app.extensions import db, migrate


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URL",
            "postgresql:///mastermind_db",
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import routes

    app.register_blueprint(routes)

    return app
