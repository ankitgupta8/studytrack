import streamlit as st
from models import db, User
from flask_login import LoginManager
from app_init import get_app_context

login_manager = LoginManager()

def init_auth():
    """Initialize authentication and session state variables"""
    # Initialize authentication state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # Initialize other session state variables
    if 'subjects' not in st.session_state:
        st.session_state.subjects = []

    if 'chapters' not in st.session_state:
        st.session_state.chapters = {}

def login_user(username, password):
    with get_app_context():
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            st.session_state.user_id = user.id
            return True
    return False

def logout_user():
    st.session_state.user_id = None
    st.session_state.subjects = []
    st.session_state.chapters = {}

def register_user(username, password):
    with get_app_context():
        if User.query.filter_by(username=username).first():
            return False

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True

def get_current_user():
    if st.session_state.user_id:
        with get_app_context():
            return User.query.get(st.session_state.user_id)
    return None

def render_auth_page():
    st.title("Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if login_user(login_username, login_password):
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.header("Register")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if reg_password != reg_confirm_password:
                st.error("Passwords do not match")
            elif register_user(reg_username, reg_password):
                st.success("Registration successful! Please login.")
                st.rerun()
            else:
                st.error("Username already exists")