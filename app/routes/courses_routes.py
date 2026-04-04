from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from app.models.courses import Course
from database import db_session
from flask_jwt_extended import jwt_required
from app.utils import role_required

course_bp = Blueprint("courses", __name__)

@course_bp.route("", methods=["GET"])
@jwt_required()
@role_required("student","admin")
def get_all_courses():
    courses = Course.query.all()
    result = []
    for c in courses:
        result.append({
            'id': c.id, 
            'name': c.name, 
            'credits': c.credits, 
            'students': [{'id': s.id, 'name': s.name} for s in c.students]
        })
    return jsonify(result), 200



@course_bp.route("/<int:course_id>", methods=["GET"])
@jwt_required()
@role_required("student","admin")
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404, description="Course not found")
    return jsonify({
        'id': course.id, 
        'name': course.name, 
        'credits': course.credits, 
        'students': [{'id': s.id, 'name': s.name} for s in course.students]
    }), 200

@course_bp.route("", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_course():
    data = request.get_json()
    if not data or not data.get("name") or "credits" not in data:
        abort(400, description="Invalid data: 'name' and 'credits' are required")
        
    try:
        new_course = Course(name=data["name"], credits=data["credits"])
        db_session.add(new_course)
        db_session.commit()
        return jsonify({
            'id': new_course.id, 
            'name': new_course.name, 
            'credits': new_course.credits, 
            'students': [{'id': s.id, 'name': s.name} for s in new_course.students]
        }), 201
    except Exception as e:
        db_session.rollback()
        abort(500, description="Database error occurred")

@course_bp.route("/<int:course_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404, description="Course not found")
        
    data = request.get_json()
    if not data or not data.get("name") or "credits" not in data:
        abort(400, description="Invalid data: 'name' and 'credits' are required")
        
    try:
        course.name = data["name"]
        course.credits = data["credits"]
        db_session.commit()
        return jsonify({
            'id': course.id, 
            'name': course.name, 
            'credits': course.credits, 
            'students': [{'id': s.id, 'name': s.name} for s in course.students]
        }), 200
    except Exception as e:
        db_session.rollback()
        abort(500, description="Database error occurred")

@course_bp.route("/<int:course_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404, description="Course not found")
        
    try:
        db_session.delete(course)
        db_session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        db_session.rollback()
        abort(500, description="Database error occurred")

@course_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return jsonify(error=e.name, description=e.description), e.code

