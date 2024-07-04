import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    DATABASE_URL = os.environ.get('DATABASE_URL') 
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_APP='app'

