import streamlit as st
from utils.data_manager import add_chapter, get_user_subjects, get_subject_chapters

def render_chapter_manager():
    """Render the chapter management interface"""
    st.header("📖 Chapter Management")

    subjects = get_user_subjects()
    if not subjects:
        st.warning("Please add subjects before managing chapters.")
        return

    # Add new chapter
    with st.form("add_chapter_form"):
        st.subheader("Add New Chapter")
        subject = st.selectbox(
            "Select Subject",
            options=[s.name for s in subjects]
        )

        chapter_name = st.text_input("Chapter Name")
        chapter_description = st.text_area("Description")
        lecture_count = st.number_input("Number of Lectures", min_value=1, value=1)

        submit_button = st.form_submit_button("Add Chapter")
        if submit_button and chapter_name:
            if add_chapter(subject, chapter_name, chapter_description, lecture_count):
                st.success(f"Chapter '{chapter_name}' added to '{subject}'!")
            else:
                st.error(f"Chapter '{chapter_name}' already exists in '{subject}'!")

    # List existing chapters by subject
    st.subheader("Existing Chapters")

    selected_subject = st.selectbox(
        "View chapters for subject",
        options=[s.name for s in subjects],
        key="view_chapters"
    )

    chapters = get_subject_chapters(selected_subject)

    if not chapters:
        st.info(f"No chapters added yet for {selected_subject}.")
    else:
        for chapter in chapters:
            with st.expander(f"📚 {chapter.name}"):
                st.write(f"**Description:** {chapter.description}")
                st.write(f"**Added on:** {chapter.created_at.strftime('%Y-%m-%d')}")
                st.write(f"**Number of Lectures:** {chapter.lecture_count}")