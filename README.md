# EduSpace Student Management Dashboard Pro

A Flask + SQLAlchemy student management system with:

- Role-based JWT authentication (admin, instructor, student)
- Many-to-many student-course enrollment API
- Profile picture upload
- Search and pagination across listing endpoints
- Admin, instructor, and student dashboard pages (Jinja + Bootstrap)
- Automated tests with pytest

This project uses a modular blueprint-based architecture and is designed as a Week 9 capstone expansion.

## Highlights

- Application factory pattern with blueprints
- Relational model design with cascade-aware foreign keys
- Enrollment uniqueness enforced at database level
- Student deletion removes linked user account
- Custom 404 and 500 error pages
- CI workflow for lint + tests

## Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- SQLite
- Jinja2 + Bootstrap + vanilla JavaScript
- pytest + pytest-cov + flake8

## Project Structure

Top-level modules:

- app/: Flask app package (routes, models, templates, static)
- tests/: API test suite
- run.py: dev server entry point
- seed.py: reset + seed script
- database.py: engine/session/base setup

## Data Model

Core entities:

- User
  - Unique username and email
  - Role: admin, instructor, student
  - Active flag for approval workflow
  - Optional profile picture URL
- Student
  - One-to-one with User
  - GPA and many-to-many courses via Enrollment
- Instructor
  - One-to-one with User
  - Major and one-to-many courses
- Course
  - Name, credits, instructor
- Enrollment
  - student_id + course_id unique pair
  - Junction table between students and courses

Important behavior:

- Student deletion removes the linked user account
- Cascade behavior is enabled with SQLite foreign keys turned on

## API Overview

Base API prefix: /api

Authentication:

- POST /api/auth/register
- POST /api/auth/login

Students:

- GET /api/students
  - Roles: admin, instructor
  - Query params: q, page, per_page
- GET /api/students/me
  - Role: student
- GET /api/students/<student_id>
  - Roles: admin, student (self)
- GET /api/students/<student_id>/courses
  - Roles: admin, student (self)
- POST /api/students
  - Role: admin
- PUT /api/students/<student_id>
  - Roles: admin, student (self)
- DELETE /api/students/<student_id>
  - Role: admin
  - Deletes student and associated user

Instructors:

- GET /api/instructors
  - Roles: admin, instructor, student
  - Query params: q, page, per_page
- GET /api/instructors/me
  - Role: instructor
- GET /api/instructors/me/courses
  - Role: instructor
  - Query params: q, page, per_page
- GET /api/instructors/<instructor_id>
  - Roles: admin, instructor, student
- POST /api/instructors
  - Role: admin
- PUT /api/instructors/<instructor_id>
  - Role: admin
- DELETE /api/instructors/<instructor_id>
  - Role: admin

Courses:

- GET /api/courses
  - Roles: admin, instructor, student
  - Query params: q, page, per_page
- GET /api/courses/<course_id>
  - Roles: admin, instructor, student
- POST /api/courses
  - Role: admin
- PUT /api/courses/<course_id>
  - Role: admin
- DELETE /api/courses/<course_id>
  - Role: admin

Enrollments:

- POST /api/enrollments
  - Roles: admin, student
  - Admin payload includes student_id and course_id
  - Student payload includes course_id
- DELETE /api/enrollments/<student_id>/<course_id>
  - Roles: admin, student (self)

Users:

- POST /api/users/profile_pic
  - JWT required
  - Multipart form upload (image file)
- GET /api/users/pending
  - Role: admin
- POST or PUT /api/users/<user_id>/approve
  - Role: admin

## Setup

1. Clone and enter the repository

   git clone <your-repo-url>
   cd python-training-w8d1

2. Create and activate virtual environment

   Windows:
   python -m venv .venv
   .venv\Scripts\activate

   Mac/Linux:
   python3 -m venv .venv
   source .venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt

4. Seed database (resets app.db)

   python seed.py

5. Run app

   python run.py

App URL: http://127.0.0.1:5000

## Seed Data Notes

- The seed script recreates the schema and inserts sample users/courses.
- Default seeded password is controlled by environment variable:
  - SEED_DEFAULT_PASSWORD (default: password123)

## Testing

Run all tests:

python -m pytest -q

Run with coverage:

python -m pytest --cov=app --cov-report=term-missing

Run lint:

python -m flake8 app tests

## CI

GitHub Actions workflow runs lint and tests on pushes/PRs for main and dev.

## Pagination and Validation Rules

- page and per_page must be >= 1 on paginated endpoints.
- Invalid pagination inputs return 400.

## Error Handling

- JSON error responses for API route exceptions
- Custom templates for web 404 and 500 pages

## Troubleshooting

If pytest reports ModuleNotFoundError: No module named app:

- Run tests from project root
- Use the workspace venv interpreter explicitly:
  d:/training/python-training-w8d1/.venv/Scripts/python.exe -m pytest -q

If login fails for seeded users:

- Rerun seeding: python seed.py
- Ensure you are using the correct seed password (SEED_DEFAULT_PASSWORD)

## Current Status

- Tests passing locally
- Role-based workflows functional for admin, instructor, and student
- Core Week 9 backend features implemented
