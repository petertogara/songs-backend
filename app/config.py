import os

class Config:
    """ Base config."""
    DEBUG = os.getenv('FLASK_DEBUG', True)
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/songs_db')
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_MASK_SWAGGER = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    TESTING = False

class TestConfig:
    MONGO_URI = "mongodb://mongodb:27017/songs_db"  

