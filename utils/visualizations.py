import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_manager import get_subject_progress, get_chapter_progress, get_user_subjects, get_subject_chapters

def create_progress_chart(subject_name):
    """Create a progress chart for a subject"""
    chapters = get_subject_chapters(subject_name)
    if not chapters:
        return None

    progress_data = []
    for chapter in chapters:
        progress_percentage = get_chapter_progress(subject_name, chapter.name)
        progress_data.append({
            'Chapter': chapter.name,
            'Progress': progress_percentage
        })

    if progress_data:
        df = pd.DataFrame(progress_data)
        fig = px.bar(
            df,
            x='Chapter',
            y='Progress',
            title=f'Progress by Chapter - {subject_name}',
            labels={'Progress': 'Completion %'}
        )
        fig.update_layout(yaxis_range=[0, 100])
        return fig
    return None

def get_overall_progress():
    """Calculate overall progress across all subjects"""
    subjects = get_user_subjects()
    if not subjects:
        return 0.0

    total_progress = 0.0
    for subject in subjects:
        total_progress += get_subject_progress(subject.name)

    return total_progress / len(subjects)

def render_dashboard():
    """Render the main dashboard with visualizations"""
    st.header("📊 Dashboard")

    # Get subjects directly from database
    subjects = get_user_subjects()
    if not subjects:
        st.warning("No subjects added yet. Please add subjects to see the dashboard.")
        return

    # Overall progress across all subjects
    overall_progress = get_overall_progress()
    st.subheader("📚 Overall Progress")
    st.progress(overall_progress / 100)
    st.write(f"Total Progress: {overall_progress:.1f}%")

    # Subject-wise progress
    st.subheader("📈 Progress by Subject")
    progress_data = []
    for subject in subjects:
        progress = get_subject_progress(subject.name)
        progress_data.append({
            'Subject': subject.name,
            'Progress': progress
        })

    if progress_data:
        df = pd.DataFrame(progress_data)

        # Create overall progress chart
        fig = px.pie(
            df,
            values='Progress',
            names='Subject',
            title='Progress Distribution by Subject'
        )
        st.plotly_chart(fig)

    # Individual subject progress
    st.subheader("📊 Chapter-wise Progress")
    for subject in subjects:
        progress_chart = create_progress_chart(subject.name)
        if progress_chart:
            st.plotly_chart(progress_chart)