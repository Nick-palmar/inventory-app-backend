from dotenv import load_dotenv
import os

class Config(object):
    load_dotenv()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')