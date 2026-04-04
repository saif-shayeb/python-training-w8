from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from app.models.student import Student
from app.models.courses import Course
from app.models.enrollment import Enrollment
from database import db_session
from flask_jwt_extended import jwt_required
from app.utils import role_required

enrollment_bp = Blueprint("enrollments", __name__)

@enrollment_bp.route("", methods=["POST"])
@jwt_required()
@role_required("admin")
def enroll_student():
    data = request.get_json()
    if not data or not data.get("student_id") or not data.get("course_id"):
        abort(400, description="Invalid data: 'student_id' and 'course_id' are required")
        
    student = Student.query.get(data["student_id"])
    course = Course.query.get(data["course_id"])
    
    if not student or not course:
        abort(404, description="Student or Course not found")
        
    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()
    if existing:
        abort(400, description="Student is already enrolled in this course")
        
    # Create manual enrollment
    enrollment = Enrollment(student_id=student.id, course_id=course.id)
    db_session.add(enrollment)
    db_session.commit()
    
    return jsonify({"message": f"Successfully enrolled {student.name} in {course.name}"}), 201

@enrollment_bp.route("/<int:student_id>/<int:course_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def drop_student(student_id, course_id):
    enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if not enrollment:
        abort(404, description="Enrollment record not found")
        
    db_session.delete(enrollment)
    db_session.commit()
    return jsonify({"message": "Enrollment removed successfully"}), 200

@enrollment_bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=e.name, description=e.description), e.code
