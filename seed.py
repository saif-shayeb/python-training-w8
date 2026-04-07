from app.models.user import User
from app.models.student import Student
from app.models.courses import Course
from database import db_session, init_db, Base, engine
from werkzeug.security import generate_password_hash
import os

def seed_database():
    # Import the models to map them to Base
    __import__("app.models.user")
    __import__("app.models.courses")
    __import__("app.models.enrollment")
    __import__("app.models.student")
    __import__("app.models.instructor")

    # Drop all tables first to apply schema changes like adding new columns
    Base.metadata.drop_all(bind=engine)
    # Re-create all tables
    init_db()

    print("Cleaning up old data...")
    Student.query.delete()
    Course.query.delete()
    User.query.delete()
    db_session.commit()

    print("Seeding Users...")
    admin_user = User(
        username="admin_test",   
        password=generate_password_hash("password123"),
        email="admin@school.edu",
        role="admin",
        is_active=True
    )
    
    student_user_1 = User(
        username="john_doe",
        password=generate_password_hash("password123"),
        email="john@school.edu",
        role="student",
        is_active=True
    )

    instructor_user_1 = User(
        username="jane_smith",
        password=generate_password_hash("password123"),
        email="jane@school.edu",
        role="instructor",
        is_active=True
    )

    db_session.add(admin_user)
    db_session.add(student_user_1)
    db_session.add(instructor_user_1)
    db_session.commit()

    from app.models.instructor import Instructor
    print("Seeding Instructor...")
    instructor_1 = Instructor(
        name="Jane Smith",
        major="Computer Science",
        user_id=instructor_user_1.id
    )
    db_session.add(instructor_1)
    db_session.commit()

    print("Seeding Courses...")
    course_math = Course(name="Mathematics 101", credits=3, instructor_id=instructor_1.id)
    course_cs = Course(name="Computer Science 101", credits=4, instructor_id=instructor_1.id)
    db_session.add(course_math)
    db_session.add(course_cs)
    db_session.commit()

    print("Seeding Students...")
    student_1 = Student(
        name="John Doe",
        gpa=3.8,
        user_id=student_user_1.id,
        courses=[course_math, course_cs]
    )
    
    db_session.add(student_1)
    db_session.commit()

    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
