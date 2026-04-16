import os

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

# CORS settings
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST', "['http://localhost:3000']")

# AI models settings
AI_MODELS_PATH = os.getenv('AI_MODELS_PATH', './models/')
