from flask import Flask
from app.routes import routes

def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(routes)
    return app