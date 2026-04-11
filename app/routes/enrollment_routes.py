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
@role_required("admin", "student")
def enroll_student():
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User

    current_user_id = int(get_jwt_identity())
    user = db_session.get(User, current_user_id)
    if not user:
        abort(401, description="Invalid user identity")

    data = request.get_json()
    if not data or not data.get("course_id"):
        abort(400, description="Course ID is required")

    # Determine which student is being enrolled
    if user.role == "student":
        student = Student.query.filter_by(user_id=user.id).first()
    else:
        # Admin can specify student_id
        if not data.get("student_id"):
            abort(400, description="Student ID is required for administrative enrollment")
        student = db_session.get(Student, data["student_id"])

    course = db_session.get(Course, data["course_id"])
    if not student or not course:
        abort(404, description="Student or Course record not found")

    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()
    if existing:
        return jsonify({"message": "Enrollment already exists"}), 200

    new_enrollment = Enrollment(student_id=student.id, course_id=course.id)
    db_session.add(new_enrollment)
    db_session.commit()

    return jsonify({"id": new_enrollment.id, "message": "Enrollment successful"}), 201


@enrollment_bp.route("/<int:student_id>/<int:course_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin", "student")
def drop_student(student_id, course_id):
    from flask_jwt_extended import get_jwt_identity
    from app.models.user import User

    current_user_id = int(get_jwt_identity())
    user = db_session.get(User, current_user_id)
    if not user:
        abort(401, description="Invalid user identity")

    target_student = db_session.get(Student, student_id)
    if not target_student:
        abort(404, description="Student not found")

    # Check permissions: Admin can drop anyone; Students can only drop themselves
    if user.role != "admin" and target_student.user_id != user.id:
        abort(403, description="Unauthorized to drop this student")

    enrollment = Enrollment.query.filter_by(
        student_id=target_student.id,
        course_id=course_id).first()
    if not enrollment:
        abort(404, description="Enrollment record not found")

    db_session.delete(enrollment)
    db_session.commit()
    return jsonify({"message": "Successfully dropped course"}), 200


@enrollment_bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=e.name, description=e.description), e.code
