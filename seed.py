import os

from app.models.user import User
from app.models.student import Student
from app.models.courses import Course
from app.models.instructor import Instructor
from database import db_session, init_db, Base, engine
from werkzeug.security import generate_password_hash


SEED_DEFAULT_PASSWORD = os.getenv("SEED_DEFAULT_PASSWORD", "password123")


def build_user(username, email, role, is_active=True):
    return User(
        username=username,
        password=generate_password_hash(SEED_DEFAULT_PASSWORD),
        email=email,
        role=role,
        is_active=is_active,
    )


def seed_database():
    # Import all models so metadata is complete before recreate.
    __import__("app.models.user")
    __import__("app.models.courses")
    __import__("app.models.enrollment")
    __import__("app.models.student")
    __import__("app.models.instructor")

    print("Resetting database schema...")
    Base.metadata.drop_all(bind=engine)
    init_db()

    print("Seeding users...")
    admin_user = build_user("admin_test", "admin@school.edu", "admin", True)

    active_student_users = [
        build_user("john_doe", "john@school.edu", "student", True)
    ] + [
        build_user(f"student_{i:02d}", f"student{i:02d}@school.edu", "student", True)
        for i in range(2, 25)
    ]

    active_instructor_users = [
        build_user("jane_smith", "jane@school.edu", "instructor", True)
    ] + [
        build_user(
            f"instructor_{i:02d}",
            f"instructor{i:02d}@school.edu",
            "instructor",
            True,
        )
        for i in range(2, 13)
    ]

    pending_student_users = [
        build_user(
            f"pending_student_{i:02d}",
            f"pending.student{i:02d}@school.edu",
            "student",
            False,
        )
        for i in range(1, 4)
    ]

    pending_instructor_users = [
        build_user(
            f"pending_instructor_{i:02d}",
            f"pending.instructor{i:02d}@school.edu",
            "instructor",
            False,
        )
        for i in range(1, 3)
    ]

    all_users = [
        admin_user,
        *active_student_users,
        *active_instructor_users,
        *pending_student_users,
        *pending_instructor_users,
    ]
    db_session.add_all(all_users)
    db_session.commit()

    print("Seeding instructors...")
    majors = [
        "Computer Science",
        "Mathematics",
        "Physics",
        "Data Science",
        "Chemistry",
        "Economics",
    ]

    active_instructors = [
        Instructor(name="Jane Smith", major=majors[0], user_id=active_instructor_users[0].id)
    ] + [
        Instructor(
            name=f"Instructor {i:02d}",
            major=majors[(i - 1) % len(majors)],
            user_id=user.id,
        )
        for i, user in enumerate(active_instructor_users[1:], start=2)
    ]

    pending_instructors = [
        Instructor(
            name=f"Pending Instructor {i:02d}",
            major=majors[(i + 1) % len(majors)],
            user_id=user.id,
        )
        for i, user in enumerate(pending_instructor_users, start=1)
    ]

    db_session.add_all([*active_instructors, *pending_instructors])
    db_session.commit()

    print("Seeding courses...")
    course_titles = [
        "Mathematics 101",
        "Computer Science 101",
        "Algorithms",
        "Databases",
        "Linear Algebra",
        "Operating Systems",
        "Software Engineering",
        "Discrete Mathematics",
        "Statistics",
        "Web Development",
        "Machine Learning",
        "Artificial Intelligence",
        "Networks",
        "Cybersecurity Basics",
        "Cloud Computing",
        "Data Structures",
        "Advanced Python",
        "Object-Oriented Design",
        "Probability",
        "Numerical Methods",
        "Compilers",
        "Human Computer Interaction",
        "Mobile App Development",
        "Big Data Analytics",
        "Game Development",
        "DevOps Fundamentals",
        "Distributed Systems",
        "Information Theory",
        "Digital Logic",
        "Research Methods",
    ]

    courses = [
        Course(
            name=title,
            credits=[2, 3, 4][idx % 3],
            instructor_id=active_instructors[idx % len(active_instructors)].id,
        )
        for idx, title in enumerate(course_titles)
    ]
    db_session.add_all(courses)
    db_session.commit()

    print("Seeding students and enrollments...")
    active_students = [
        Student(
            name="John Doe",
            gpa=3.8,
            user_id=active_student_users[0].id,
            courses=[courses[0], courses[1], courses[2]],
        )
    ] + [
        Student(
            name=f"Student {i:02d}",
            gpa=round(min(4.0, 2.1 + ((i % 19) * 0.1)), 2),
            user_id=user.id,
            courses=[
                courses[(i * 2 + offset) % len(courses)]
                for offset in range(3 + (i % 3))
            ],
        )
        for i, user in enumerate(active_student_users[1:], start=2)
    ]

    pending_students = [
        Student(
            name=f"Pending Student {i:02d}",
            gpa=round(2.5 + (i * 0.2), 2),
            user_id=user.id,
            courses=[],
        )
        for i, user in enumerate(pending_student_users, start=1)
    ]

    db_session.add_all([*active_students, *pending_students])
    db_session.commit()

    print("Database seeding completed successfully!")
    print(f"Users: {User.query.count()}")
    print(f"Students: {Student.query.count()}")
    print(f"Instructors: {Instructor.query.count()}")
    print(f"Courses: {Course.query.count()}")


if __name__ == "__main__":
    seed_database()
