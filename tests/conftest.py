import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app.models.courses import Course
from app.models.instructor import Instructor
from app.models.student import Student
from app.models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from database import Base, db_session, engine
from app import create_app
import pytest


@pytest.fixture(scope="session")
def app():
    app_instance = create_app()
    app_instance.config["TESTING"] = True
    app_instance.config["UPLOAD_FOLDER"] = "/tmp/test_uploads"
    yield app_instance


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield db_session
        db_session.remove()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def seed_data(db, app):
    admin_user = User(
        username="admin_test",
        password=generate_password_hash("pwd"),
        role="admin",
        email="admin@test.com",
        is_active=True
    )
    student_user = User(
        username="student_test",
        password=generate_password_hash("pwd"),
        role="student",
        email="student@test.com",
        is_active=True
    )
    inst_user = User(
        username="inst_test",
        password=generate_password_hash("pwd"),
        role="instructor",
        email="inst@test.com",
        is_active=True
    )
    empty_student_user = User(
        username="empty_stud",
        password=generate_password_hash("pwd"),
        role="student",
        email="empty_s@test.com",
        is_active=True
    )
    empty_inst_user = User(
        username="empty_inst",
        password=generate_password_hash("pwd"),
        role="instructor",
        email="empty_i@test.com",
        is_active=True
    )
    inactive_user = User(
        username="inactive_test",
        password=generate_password_hash("pwd"),
        role="student",
        email="inactive@test.com",
        is_active=False
    )

    db.add_all([admin_user,
                student_user,
                inst_user,
                empty_student_user,
                empty_inst_user,
                inactive_user])
    db.commit()

    instructor = Instructor(name="Dr. Test", major="CS", user_id=inst_user.id)
    db.add(instructor)
    db.commit()

    course = Course(name="Test Course 101", credits=3, instructor_id=instructor.id)
    db.add(course)
    db.commit()

    student = Student(name="Test Student", gpa=3.5, user_id=student_user.id)
    db.add(student)
    db.commit()

    admin_token = create_access_token(
        identity=str(admin_user.id), additional_claims={"role": "admin"}
    )
    student_token = create_access_token(
        identity=str(student_user.id), additional_claims={"role": "student"}
    )

    return {
        "admin_id": admin_user.id,
        "student_user_id": student_user.id,
        "empty_student_user_id": empty_student_user.id,
        "inst_user_id": inst_user.id,
        "empty_inst_user_id": empty_inst_user.id,
        "inactive_user_id": inactive_user.id,
        "instructor_id": instructor.id,
        "course_id": course.id,
        "student_id": student.id,
        "admin_token": admin_token,
        "student_token": student_token,
        "admin_headers": {"Authorization": f"Bearer {admin_token}"},
        "student_headers": {"Authorization": f"Bearer {student_token}"}
    }
