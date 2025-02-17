import streamlit as st
from app_init import init_database
from auth import init_auth, render_auth_page, get_current_user
from components.subject_manager import render_subject_manager
from components.chapter_manager import render_chapter_manager
from components.progress_tracker import render_progress_tracker
from utils.visualizations import render_dashboard
from app_init import get_app_context

def main():
    st.set_page_config(
        page_title="Lecture Progress Tracker",
        page_icon="📚",
        layout="wide"
    )

    # Initialize database
    init_database()

    # Initialize authentication
    init_auth()

    # Check if user is logged in
    with get_app_context():
        user = get_current_user()
        if not user:
            render_auth_page()
            return

        # Main title
        st.title(f"📚 Lecture Progress Tracker - Welcome, {user.username}!")

        # Logout button in sidebar
        if st.sidebar.button("Logout"):
            st.session_state.user_id = None
            st.rerun()

        # Sidebar for navigation
        page = st.sidebar.radio(
            "Navigate to",
            ["Dashboard", "Subjects", "Chapters", "Progress Tracking"]
        )

        # Page routing
        if page == "Dashboard":
            render_dashboard()
        elif page == "Subjects":
            render_subject_manager()
        elif page == "Chapters":
            render_chapter_manager()
        elif page == "Progress Tracking":
            render_progress_tracker()

if __name__ == "__main__":
    main()