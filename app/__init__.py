from flask import Flask
from .config import Config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)

    from . import db
    db.init_app(app)
    

    return app
    
