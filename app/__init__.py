import os
from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from pymongo import MongoClient
import mongomock
from .config import Config
from .api.song_routes import api as song_api
from .logging_config import setup_logging
from .utils.load_songs_init import initialize_songs_into_db
import json

def get_db_connection(app):
    """Establish a connection to the MongoDB database."""
    client = MongoClient(app.config["MONGO_URI"])  
    return client.get_default_database()

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    CORS(app)
    setup_logging(app)

    if app.config.get('TESTING'):
        
        app.db = mongomock.MongoClient().db
    else:
        
        app.db = get_db_connection(app)

    if not app.config.get('TESTING'):
        with app.app_context():
            try:
                initialize_songs_into_db(app.db) 
            except Exception as e:
                app.logger.error(f"Error initializing songs: {e}")

    api = Api(app, title="Yousians Songs API", version="1.0.0", description="API for song management")
    api.add_namespace(song_api, path='/songs')

    return app

