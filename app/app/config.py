# import os
# import datetime
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') 
#     DATABASE_URL = os.environ.get('DATABASE_URL') 
#     JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
#     FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
#     FLASK_APP='app'
#     JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)  # Durée de vie du token d'accès
#     JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)  # Durée de vie du token de rafraîchissement



from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)

# Enregistrement des blueprints
from app.users import user_bp
app.register_blueprint(user_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
