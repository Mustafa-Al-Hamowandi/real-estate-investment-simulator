import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///real_estate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # API Keys — pulled from .env, never hardcoded here
    NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')

    # Upload folder
    UPLOAD_FOLDER = 'static/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size