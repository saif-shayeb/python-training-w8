from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.user import User
from database import db_session
from app.models.student import Student
from app.models.instructor import Instructor

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    # Validate required fields
    if (
        not data
        or not data.get("username")
        or not data.get("password")
        or not data.get("role")
        or not data.get("email")
    ):
        abort(
            400,
            description="Invalid data: 'username', 'password', 'role', and 'email' are required",
        )
    if data["role"] not in ["student", "admin", "instructor"]:
        abort(400, description="Invalid data: 'role' must be 'student', 'admin' or 'instructor'")
    # Check if user already exists
    if User.query.filter_by(username=data["username"]).first():
        abort(400, description="Username already taken")

    # Hash the password securely!
    hashed_password = generate_password_hash(data["password"])

    try:
        new_user = User(
            username=data["username"],
            password=hashed_password,
            role=data["role"],
            email=data["email"],
        )
        db_session.add(new_user)
        db_session.commit()

        if data["role"] == "student":
            if not data.get("name") or "gpa" not in data:
                abort(400, description="Invalid data: 'name' and 'gpa' are required for student")
            new_student = Student(
                name=data["name"],
                gpa=data["gpa"],
                user_id=new_user.id,
                courses=[])
            db_session.add(new_student)
            db_session.commit()

        elif data["role"] == "instructor":
            if not data.get("name") or not data.get("major"):
                abort(400, description="Invalid data: 'name' and 'major' are required")
            new_instructor = Instructor(name=data["name"], major=data["major"], user_id=new_user.id)
            db_session.add(new_instructor)
            db_session.commit()

        response_data = {
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "role": new_user.role,
                "email": new_user.email,
            },
        }

        if data["role"] == "student":
            response_data["student"] = {
                "id": new_student.id,
                "name": new_student.name,
                "gpa": new_student.gpa,
            }
        elif data["role"] == "instructor":
            response_data["instructor"] = {
                "id": new_instructor.id,
                "name": new_instructor.name,
                "major": new_instructor.major,
            }

        return jsonify(response_data), 201

    except Exception as e:
        db_session.rollback()
        abort(500, description=f"Database error occurred: {str(e)}")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        abort(400, description="Missing 'username' or 'password'")

    # Find user by username
    user = User.query.filter_by(username=data["username"]).first()

    # Check if user exists and password hash matches
    if not user or not check_password_hash(user.password, data["password"]):
        abort(401, description="Invalid username or password")

    if not user.is_active:
        abort(403, description="Account pending administrator approval")

    # Generate token containing user's identity and their role
    access_token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )

    response_data = {
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "email": user.email,
        },
    }

    if user.role == "student" and user.student:
        response_data["student"] = {
            "id": user.student.id,
            "name": user.student.name,
            "gpa": user.student.gpa,
        }
    elif user.role == "instructor" and user.instructor:
        response_data["instructor"] = {
            "id": user.instructor.id,
            "name": user.instructor.name,
            "major": user.instructor.major,
        }

    return jsonify(response_data), 200


@auth_bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=e.name, description=e.description), e.code
