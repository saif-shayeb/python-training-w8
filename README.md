# EduSpace Student Management Dashboard Pro

Flask + SQLAlchemy web application for managing students, instructors, courses, and enrollments with role-based authentication and both API and dashboard UI experiences.

## Project Overview

EduSpace is a role-based student management platform that supports three user types:

- Admin: full management of students, instructors, courses, enrollments, and pending-user approvals.
- Instructor: profile and assigned-course access.
- Student: profile access, course catalog browsing, and self-enrollment actions.

Core capabilities:

- JWT authentication and role authorization.
- CRUD APIs for students, instructors, and courses.
- Enrollment API with duplicate-enrollment protection.
- Profile picture upload endpoint.
- Dashboard routes for admin, instructor, and student UIs.
- Seed script for repeatable local demo data.
- Pytest test suite for API behavior.

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- pip

### 2. Clone and enter project

```bash
git clone <your-repo-url>
cd python-training-w8d1
```

### 3. Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Optional environment configuration

Create a `.env` file in the project root (optional defaults already exist):

```env
JWT_SECRET_KEY=replace-with-a-long-random-secret
SEED_DEFAULT_PASSWORD=password123
```

### 6. Seed the database

This resets and recreates the SQLite schema, then inserts sample data.

```bash
python seed.py
```

### 7. Run the application

```bash
python run.py
```

Open: http://127.0.0.1:5000

### 8. Run tests

```bash
python -m pytest -q
```

## Folder Structure

```text
python-training-w8d1/
|-- app/
|   |-- __init__.py
|   |-- utils.py
|   |-- models/
|   |   |-- user.py
|   |   |-- student.py
|   |   |-- instructor.py
|   |   |-- courses.py
|   |   `-- enrollment.py
|   |-- routes/
|   |   |-- auth_routes.py
|   |   |-- students_routes.py
|   |   |-- instructors_routes.py
|   |   |-- courses_routes.py
|   |   |-- enrollment_routes.py
|   |   |-- users_routes.py
|   |   `-- web_routes.py
|   |-- static/
|   |   |-- app.js
|   |   |-- styles.css
|   |   `-- uploads/profile_pics/
|   `-- templates/
|       |-- admin/
|       |-- instructor/
|       |-- student/
|       |-- public/
|       |-- shared/
|       `-- errors/
|-- tests/
|   |-- conftest.py
|   |-- test_auth_api.py
|   |-- test_students_api.py
|   |-- test_instructors_enrollment_api.py
|   |-- test_courses_api.py
|   `-- test_users_api.py
|-- config.py
|-- database.py
|-- run.py
|-- seed.py
|-- requirements.txt
`-- README.md
```

## Screenshots

Current sample screenshot:
<img width="1915" height="966" alt="image" src="https://github.com/user-attachments/assets/5f2473f5-4c6c-4f0f-8b06-73f3ad250dc1" />
<img width="1919" height="970" alt="image" src="https://github.com/user-attachments/assets/6dc30d93-1f77-4a07-8e90-ccdceda39c8b" />
<img width="1919" height="966" alt="image" src="https://github.com/user-attachments/assets/d3a954a3-7b7b-43f3-b166-9ec09d05a893" />
<img width="1919" height="966" alt="image" src="https://github.com/user-attachments/assets/67d13b73-3cee-43b1-8706-3a0ec4b13b60" />
<img width="1892" height="954" alt="image" src="https://github.com/user-attachments/assets/ef987fe6-2d0a-42ca-bd2e-5bc32fff13cc" />
<img width="1919" height="920" alt="image" src="https://github.com/user-attachments/assets/c61e1bd1-89a1-4882-8d50-22a0c83a943f" />


Recommended additions:

- Login page screenshot
- Admin dashboard screenshot
- Student dashboard screenshot
- Instructor courses screenshot

## API Reference

Base API URL: `/api`

Authentication:

- JWT token required for protected endpoints.
- Send token in header: `Authorization: Bearer <token>`

### Auth

| Method | Endpoint           | Description                              | Auth   |
| ------ | ------------------ | ---------------------------------------- | ------ |
| POST   | /api/auth/register | Register user (student/admin/instructor) | Public |
| POST   | /api/auth/login    | Login and receive JWT token              | Public |

### Students

| Method | Endpoint                           | Description                         | Roles                 |
| ------ | ---------------------------------- | ----------------------------------- | --------------------- |
| GET    | /api/students                      | List students (search + pagination) | admin, instructor     |
| GET    | /api/students/me                   | Get current student profile         | student               |
| GET    | /api/students/{student_id}         | Get one student                     | admin, student (self) |
| GET    | /api/students/{student_id}/courses | Get student courses                 | admin, student (self) |
| POST   | /api/students                      | Create student                      | admin                 |
| PUT    | /api/students/{student_id}         | Update student                      | admin, student (self) |
| DELETE | /api/students/{student_id}         | Delete student and linked user      | admin                 |

### Instructors

| Method | Endpoint                         | Description                                  | Roles                      |
| ------ | -------------------------------- | -------------------------------------------- | -------------------------- |
| GET    | /api/instructors                 | List instructors (search + pagination)       | admin, student, instructor |
| GET    | /api/instructors/me              | Get current instructor profile               | instructor                 |
| GET    | /api/instructors/me/courses      | Get instructor courses (search + pagination) | instructor                 |
| GET    | /api/instructors/{instructor_id} | Get one instructor                           | admin, student, instructor |
| POST   | /api/instructors                 | Create instructor                            | admin                      |
| PUT    | /api/instructors/{instructor_id} | Update instructor                            | admin                      |
| DELETE | /api/instructors/{instructor_id} | Delete instructor                            | admin                      |

### Courses

| Method | Endpoint                 | Description                        | Roles                      |
| ------ | ------------------------ | ---------------------------------- | -------------------------- |
| GET    | /api/courses             | List courses (search + pagination) | admin, student, instructor |
| GET    | /api/courses/{course_id} | Get one course                     | admin, student, instructor |
| POST   | /api/courses             | Create course                      | admin                      |
| PUT    | /api/courses/{course_id} | Update course                      | admin                      |
| DELETE | /api/courses/{course_id} | Delete course                      | admin                      |

### Enrollments

| Method | Endpoint                                  | Description              | Roles                 |
| ------ | ----------------------------------------- | ------------------------ | --------------------- |
| POST   | /api/enrollments                          | Enroll student in course | admin, student        |
| DELETE | /api/enrollments/{student_id}/{course_id} | Drop enrollment          | admin, student (self) |

### Users

| Method   | Endpoint                     | Description                               | Roles                  |
| -------- | ---------------------------- | ----------------------------------------- | ---------------------- |
| POST     | /api/users/profile_pic       | Upload profile picture (multipart `file`) | any authenticated user |
| GET      | /api/users/pending           | List inactive users                       | admin                  |
| POST/PUT | /api/users/{user_id}/approve | Approve user account                      | admin                  |

### Query Parameters

Used on list endpoints:

- `q`: case-insensitive search text
- `page`: page number (must be >= 1)
- `per_page`: items per page (must be >= 1)

## Deployment Link

- Current local deployment: http://127.0.0.1:5000
- Production deployment: add your hosted URL here (https://python-training-w8.onrender.com)
