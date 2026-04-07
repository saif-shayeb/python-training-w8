# 🎓 EduSpace Student Portal API

Welcome to the **EduSpace Student Portal API**, a fully modular and professionally deployed RESTful API with a stunning front-end Dashboard interface.

Built during Week 8 of Python Training, this project seamlessly combines modern API best-practices, encrypted token security, and rich Jinja templating.

## 🌟 Key Features
- **Application Factory Pattern:** Scalable `create_app()` architecture utilizing Flask Blueprints for extreme modularity.
- **Role-Based Token Authentication:** Armed with `flask-jwt-extended` to ensure routes are strictly protected by User Roles (`admin` vs `student`).
- **Relational Data Mapping:** Robust SQLite schemas establishing One-To-One (`User` ↔ `Student`) and Many-To-Many (`Student` ↔ `Course`) relationships using pure SQLAlchemy.
- **Immaculate UI/UX:** Built-in Administrator Dashboard rendered globally over Jinja (`/` route). We didn't settle for boring; it utilizes cutting-edge Vanilla CSS Glassmorphism, tailored hex pallets, smooth dynamic micro-animations, and responsive layout grids.
- **Automated Validation:** Comes fully fortified with a `unittest` + Flask Test Client testing suite completely covering core REST actions (`GET`, `POST`, `PUT`, `DELETE`).

---

## 📸 Screenshots (Replace these before submitting!)

> To pass your assignment, take a screenshot of your beautiful Jinja Dashboard and of a successful Postman API call, and paste them here!

![Dashboard UI Placeholder](https://via.placeholder.com/800x400?text=Paste+your+Jinja+Dashboard+Screenshot+Here)
![Postman Test Placeholder](https://via.placeholder.com/800x400?text=Paste+your+Postman+API+Test+Here)

---

## 🗄️ Database Schema

The system is built on a relational SQLite database managed by SQLAlchemy.

### Core Models
- **User**: Stores authentication credentials.
  - `id` (Integer, PK): Unique identifier.
  - `username` (String): Unique login name.
  - `password` (String): Securely hashed password.
  - `role` (String): Role-based access control (`admin`, `student`, `instructor`).
  - `email` (String): Primary contact email.
- **Student**: profile linked to a User.
  - `user_id` (FK): Links to `Users.id`.
  - `name` (String): Full student name.
  - `gpa` (Float): Academic performance metric.
- **Instructor**: Profile linked to a User.
  - `user_id` (FK): Links to `Users.id`.
  - `name` (String): Instructor name.
  - `major` (String): Department/Specialization.
- **Course**: Academic offerings.
  - `instructor_id` (FK): Links to `Instructors.id`.
  - `name` (String): Title of the course.
  - `credits` (Integer): Credit value.
- **Enrollment** (Junction Table): Manages Many-to-Many relationship between Students and Courses.

---

## 🚀 API Documentation

All API endpoints require a `JWT Bearer Token` in the `Authorization` header unless otherwise specified. Base URL: `/api`.

### 🔐 Authentication (`/auth`)
| Method | Endpoint | Payload | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | `{username, password, role, email, ...}` | Create a new user and profile. |
| `POST` | `/login` | `{username, password}` | Generate access token. |

### 👨‍🎓 Students (`/students`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Admin, Instructor | List all students (**Query params:** `q`, `page`, `per_page`). |
| `GET` | `/me` | Student | Retrieve own profile data. |
| `GET` | `/<id>` | Admin, Self | Get detailed student record. |
| `PUT` | `/<id>` | Admin, Self | Update student information. |
| `DELETE` | `/<id>` | Admin | Permanently remove student and associated user. |

### 👨‍🏫 Instructors (`/instructors`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | All | List all instructors (**Query params:** `q`, `page`, `per_page`). |
| `GET` | `/me` | Instructor | Retrieve own instructor profile. |
| `GET` | `/<id>` | All | Get detailed instructor record. |
| `POST` | `/` | Admin | Manually create instructor profile. |
| `PUT` | `/<id>` | Admin | Update instructor specialization/major. |

### 📚 Courses (`/courses`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | All | List all available courses (**Query params:** `q`, `page`, `per_page`). |
| `GET` | `/<id>` | All | Get specific course details. |
| `POST` | `/` | Admin | Add a new course to the catalog. |
| `PUT` | `/<id>` | Admin | Update name, credits, or instructor. |
| `DELETE` | `/<id>` | Admin | Archive/Remove course. |

### 📝 Enrollments (`/enrollments`)
| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Admin, Student | Enroll student in a course (body: `{course_id, student_id?}`). |
| `DELETE` | `/<sid>/<cid>` | Admin, Student | Remove student from a specific course. |

---

## 🛠 Setup & Installation

Follow these steps to boot the application up natively on your machine!

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd python-training-w8d1
```

### 2. Prepare the Virtual Environment
Create and activate an isolated Python container:
**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Seeding
To immediately populate your local database with dummy users, students, and active courses, run the built-in CLI seeder:
```bash
python seed.py
```
*(This will safely reset the `app.db` and output `admin_test` / `john_doe`!)*

### 5. Start the Server
To launch the production-ready instance (or development server):
```bash
python run.py
```
*(Waitress / Gunicorn will be activated depending on your environment logic, or standard Flask via localhost:5000).*

---

## 🧪 Running the Test Suite
The repository maintains full automated test coverage over its endpoints using the bundled `flask.testing` framework. 

To execute the test suite, ensure your `.venv` is activated and type:
```bash
python -m pytest
```
*(Every single SQL transaction successfully executed by tests will gracefully rollback using `PendingRollbackError` prevention!)*

## ☁️ Deployment Ready
This repository comes dynamically prepped for Render.com hosting seamlessly leveraging `gunicorn`, `.env` OS Environment hooks mapped to SQLite defaults, and declarative package freezing (`requirements.txt`). Just point a Render Web Service to the repo and you're magically live!
