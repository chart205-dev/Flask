import os
from datetime import timedelta


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_ECHO = True

class DevelopmentConfig(Config):
     SQLALCHEMY_DATABASE_URI = "postgresql://postgres:pass@localhost:5432/flask_api_db"
     DEBUG = True
     TESTING = False

config = {
    'development': DevelopmentConfig
}