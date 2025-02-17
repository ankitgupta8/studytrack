from models import db, Subject, Chapter, Progress
from auth import get_current_user
from app_init import get_app_context
import json

def add_subject(subject_name, description=""):
    """Add a new subject to the database"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return False

        existing = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if existing:
            return False

        subject = Subject(name=subject_name, description=description, user_id=user.id)
        db.session.add(subject)
        db.session.commit()
        return True

def add_chapter(subject_name, chapter_name, description="", lecture_count=1):
    """Add a new chapter to a subject"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return False

        subject = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if not subject:
            return False

        existing = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
        if existing:
            return False

        chapter = Chapter(
            name=chapter_name,
            description=description,
            lecture_count=lecture_count,
            subject_id=subject.id
        )
        db.session.add(chapter)

        # Initialize progress
        progress = Progress(
            chapter=chapter,
            lectures=json.dumps([False] * lecture_count)
        )
        db.session.add(progress)

        db.session.commit()
        return True

def update_progress(subject_name, chapter_name, progress_data):
    """Update progress for a specific chapter"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return False

        subject = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if not subject:
            return False

        chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
        if not chapter:
            return False

        progress = chapter.progress
        if not progress:
            progress = Progress(chapter=chapter)
            db.session.add(progress)

        progress.set_lecture_states(progress_data['lectures'])
        progress.dpp = progress_data['dpp']
        progress.revision = progress_data['revision']
        progress.pyq = progress_data['pyq']
        progress.tests = progress_data['tests']

        db.session.commit()
        return True

def get_chapter_progress(subject_name, chapter_name):
    """Calculate progress percentage for a specific chapter"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return 0.0

        subject = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if not subject:
            return 0.0

        chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
        if not chapter or not chapter.progress:
            return 0.0

        progress = chapter.progress
        lecture_states = progress.get_lecture_states()
        total_items = len(lecture_states) + 4  # lectures + dpp + revision + pyq + tests
        completed_items = sum(lecture_states) + sum([
            progress.dpp,
            progress.revision,
            progress.pyq,
            progress.tests
        ])
        return (completed_items / total_items) * 100

def get_subject_progress(subject_name):
    """Calculate overall progress for a subject"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return 0.0

        subject = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if not subject:
            return 0.0

        chapters = Chapter.query.filter_by(subject_id=subject.id).all()
        if not chapters:
            return 0.0

        total_progress = sum(get_chapter_progress(subject_name, chapter.name)
                            for chapter in chapters)
        return total_progress / len(chapters)

def delete_subject(subject_name):
    """Delete a subject and its related chapters"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return False

        subject = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if subject:
            db.session.delete(subject)  # This will cascade delete chapters and progress
            db.session.commit()
            return True
        return False

def get_user_subjects():
    """Get all subjects for the current user"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return []
        return Subject.query.filter_by(user_id=user.id).all()

def get_subject_chapters(subject_name):
    """Get all chapters for a subject"""
    with get_app_context():
        user = get_current_user()
        if not user:
            return []

        subject = Subject.query.filter_by(name=subject_name, user_id=user.id).first()
        if not subject:
            return []

        return Chapter.query.filter_by(subject_id=subject.id).all()