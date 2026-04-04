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
