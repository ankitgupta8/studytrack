import streamlit as st
from utils.data_manager import add_subject, delete_subject, get_user_subjects

def render_subject_manager():
    """Render the subject management interface"""
    st.header("📚 Subject Management")

    # Add new subject
    with st.form("add_subject_form"):
        st.subheader("Add New Subject")
        subject_name = st.text_input("Subject Name")
        subject_description = st.text_area("Description")

        submit_button = st.form_submit_button("Add Subject")
        if submit_button and subject_name:
            if add_subject(subject_name, subject_description):
                st.success(f"Subject '{subject_name}' added successfully!")
            else:
                st.error(f"Subject '{subject_name}' already exists!")

    # List and manage existing subjects
    st.subheader("Existing Subjects")
    subjects = get_user_subjects()

    if not subjects:
        st.info("No subjects added yet. Add your first subject above!")
    else:
        for subject in subjects:
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{subject.name}**")
                st.write(subject.description)

            with col2:
                st.write(f"Created: {subject.created_at.strftime('%Y-%m-%d')}")

            with col3:
                if st.button("Delete", key=f"delete_{subject.name}"):
                    if delete_subject(subject.name):
                        st.success(f"Subject '{subject.name}' deleted!")
                        st.experimental_rerun()