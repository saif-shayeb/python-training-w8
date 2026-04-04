from app.models.user import User
from app.models.student import Student
from app.models.courses import Course
from database import db_session, init_db
from werkzeug.security import generate_password_hash
import os

def seed_database():
    # Attempt to initialize the db
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
        role="admin"
    )
    
    student_user_1 = User(
        username="john_doe",
        password=generate_password_hash("password123"),
        email="john@school.edu",
        role="student"
    )

    db_session.add(admin_user)
    db_session.add(student_user_1)
    db_session.commit()

    print("Seeding Courses...")
    course_math = Course(name="Mathematics 101", credits=3)
    course_cs = Course(name="Computer Science 101", credits=4)
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
