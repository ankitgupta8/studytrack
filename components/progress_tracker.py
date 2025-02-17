import streamlit as st
from utils.data_manager import update_progress, get_chapter_progress, get_user_subjects, get_subject_chapters
from app_init import get_app_context
from models import Progress, db

def render_progress_tracker():
    """Render the progress tracking interface"""
    st.header("📈 Progress Tracking")

    subjects = get_user_subjects()
    if not subjects:
        st.warning("Please add subjects and chapters before tracking progress.")
        return

    # Select subject
    subject = st.selectbox(
        "Select Subject",
        options=[s.name for s in subjects]
    )

    # Get all chapters for the selected subject
    chapters = get_subject_chapters(subject)

    if not chapters:
        st.warning(f"No chapters added for {subject} yet.")
        return

    # Create the grid-based progress tracker
    st.subheader(f"{subject} Progress Tracker")

    # Create header row
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 1, 1, 1, 1, 1, 2])
    with col1:
        st.write("**Chapters**")
    with col2:
        st.write("**Lecture**")
    with col3:
        st.write("**DPP**")
    with col4:
        st.write("**Revision**")
    with col5:
        st.write("**PYQs**")
    with col6:
        st.write("**Tests**")
    with col7:
        st.write("**Progress**")

    # Create rows for each chapter
    with get_app_context():
        for chapter in chapters:
            # Explicitly query for progress to avoid detached instance errors
            current_progress = Progress.query.filter_by(chapter_id=chapter.id).first()
            if current_progress:
                lecture_states = current_progress.get_lecture_states()
            else:
                lecture_states = [False] * chapter.lecture_count
                current_progress = Progress(chapter=chapter)
                db.session.add(current_progress)
                db.session.commit()

            col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 1, 1, 1, 1, 1, 2])

            with col1:
                st.write(chapter.name)

            with col2:
                # Create checkboxes for each lecture
                lecture_states_new = []
                for i in range(chapter.lecture_count):
                    lecture_checked = st.checkbox(
                        f"L{i+1}",
                        value=lecture_states[i] if i < len(lecture_states) else False,
                        key=f"lecture_{subject}_{chapter.name}_{i}"
                    )
                    lecture_states_new.append(lecture_checked)

            with col3:
                dpp = st.checkbox(
                    "DPP",
                    value=current_progress.dpp if current_progress else False,
                    key=f"dpp_{subject}_{chapter.name}"
                )

            with col4:
                revision = st.checkbox(
                    "Rev",
                    value=current_progress.revision if current_progress else False,
                    key=f"revision_{subject}_{chapter.name}"
                )

            with col5:
                pyq = st.checkbox(
                    "PYQ",
                    value=current_progress.pyq if current_progress else False,
                    key=f"pyq_{subject}_{chapter.name}"
                )

            with col6:
                tests = st.checkbox(
                    "Test",
                    value=current_progress.tests if current_progress else False,
                    key=f"tests_{subject}_{chapter.name}"
                )

            with col7:
                # Update progress
                new_progress = {
                    'lectures': lecture_states_new,
                    'dpp': dpp,
                    'revision': revision,
                    'pyq': pyq,
                    'tests': tests
                }
                update_progress(subject, chapter.name, new_progress)

                # Display progress percentage
                progress_percentage = get_chapter_progress(subject, chapter.name)
                st.write(f"{progress_percentage:.1f}%")
                st.progress(progress_percentage / 100)