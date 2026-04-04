from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from app.models.student import Student
from app.models.courses import Course
from database import db_session
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.utils import role_required

student_bp = Blueprint("students", __name__)

@student_bp.route("", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_all_students():
    students = Student.query.all()
    result = []
    for s in students:
        result.append({
            'id': s.id, 
            'user_id': s.user_id,
            'name': s.name, 
            'gpa': s.gpa, 
            'courses': [{'id': c.id, 'name': c.name} for c in s.courses]
        })
    return jsonify(result), 200

@student_bp.route("/me", methods=["GET"])
@jwt_required()
@role_required("student")
def get_my_profile():
    from flask_jwt_extended import get_jwt_identity
    user_id = get_jwt_identity()
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        abort(404, description="Student profile not found")
        
    return jsonify({
        'id': student.id, 
        'user_id': student.user_id,
        'name': student.name, 
        'gpa': student.gpa, 
        'courses': [{'id': c.id, 'name': c.name} for c in student.courses]
    }), 200

@student_bp.route("/<int:student_id>", methods=["GET"])
@jwt_required()
@role_required("student","admin")
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        abort(404, description="Student not found")
        
    claims = get_jwt()
    if claims.get("role") == "student" and str(student.user_id) != str(get_jwt_identity()):
        abort(403, description="Forbidden: You can only access your own profile")
        
    return jsonify({
        'id': student.id, 
        'user_id': student.user_id,
        'name': student.name, 
        'gpa': student.gpa, 
        'courses': [{'id': c.id, 'name': c.name} for c in student.courses]
    }), 200

@student_bp.route("/<int:student_id>/courses", methods=["GET"])
@jwt_required()
@role_required("student","admin")
def get_student_courses(student_id):
    student = Student.query.get(student_id)
    if not student:
        abort(404, description="Student not found")
        
    claims = get_jwt()
    if claims.get("role") == "student" and str(student.user_id) != str(get_jwt_identity()):
        abort(403, description="Forbidden: You can only access your own profile")
        
    return jsonify([{'id': c.id, 'name': c.name, 'credits': c.credits} for c in student.courses]), 200

@student_bp.route("", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_student():
    data = request.get_json()
    if not data or not data.get("name") or "gpa" not in data or "user_id" not in data:
        abort(400, description="Invalid data: 'name', 'gpa', and 'user_id' are required")
        
    try:
        new_student = Student(name=data["name"], gpa=data["gpa"], user_id=data["user_id"])
        
        # Handle courses if provided as a list of IDs
        if "courses" in data and isinstance(data["courses"], list):
            for course_id in data["courses"]:
                course = Course.query.get(course_id)
                if course:
                    new_student.courses.append(course)
                    
        db_session.add(new_student)
        db_session.commit()
        return jsonify({
            'id': new_student.id, 
            'user_id': new_student.user_id,
            'name': new_student.name, 
            'gpa': new_student.gpa, 
            'courses': [{'id': c.id, 'name': c.name} for c in new_student.courses]
        }), 201
    except Exception as e:
        db_session.rollback()
        abort(500, description="Database error occurred")

@student_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
@role_required("admin","student")
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        abort(404, description="Student not found")
        
    claims = get_jwt()
    if claims.get("role") == "student" and str(student.user_id) != str(get_jwt_identity()):
        abort(403, description="Forbidden: You can only access your own profile")
        
    data = request.get_json()
    if not data or not data.get("name") or "gpa" not in data:
        abort(400, description="Invalid data: 'name' and 'gpa' are required")
        
    try:
        student.name = data["name"]
        student.gpa = data["gpa"]
        
        # Optionally update user_id
        if "user_id" in data:
            student.user_id = data["user_id"]
            
        # Handle courses if provided
        if "courses" in data and isinstance(data["courses"], list):
            student.courses = [] # Clear existing
            for course_id in data["courses"]:
                course = Course.query.get(course_id)
                if course:
                    student.courses.append(course)
                    
        db_session.commit()
        return jsonify({
            'id': student.id, 
            'user_id': student.user_id,
            'name': student.name, 
            'gpa': student.gpa, 
            'courses': [{'id': c.id, 'name': c.name} for c in student.courses]
        }), 200
    except Exception as e:
        db_session.rollback()
        abort(500, description="Database error occurred")

@student_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        abort(404, description="Student not found")
        
    try:
        db_session.delete(student)
        db_session.commit()
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        db_session.rollback()
        abort(500, description="Database error occurred")
        
@student_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return jsonify(error=e.name, description=e.description), e.code