from flask import Flask
from models import db
import streamlit as st
import os

# Initialize Flask app for database
app = Flask(__name__)

# Use Streamlit secrets for configuration
if st.runtime.exists():
    # Production configuration (Streamlit Cloud)
    app.config['SQLALCHEMY_DATABASE_URI'] = st.secrets["database"]["url"]
    app.config['SECRET_KEY'] = st.secrets["flask"]["secret_key"]
else:
    # Local development configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///lecture_tracker.db')
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def get_app_context():
    return app.app_context()

def init_database():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()