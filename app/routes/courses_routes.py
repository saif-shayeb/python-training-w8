from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from app.models.courses import Course
from app.models.instructor import Instructor
from database import db_session
from flask_jwt_extended import jwt_required
from app.utils import role_required

course_bp = Blueprint("courses", __name__)


@course_bp.route("", methods=["GET"])
@jwt_required()
@role_required("student", "admin", "instructor")
def get_all_courses():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search_query = request.args.get("q", "", type=str)

    if page < 1 or per_page < 1:
        abort(400, description="Invalid pagination: 'page' and 'per_page' must be >= 1")

    query = Course.query
    if search_query:
        query = query.filter(Course.name.ilike(f"%{search_query}%"))

    total = query.count()
    import math
    total_pages = math.ceil(total / per_page)

    courses = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for c in courses:
        result.append(
            {
                "id": c.id,
                "name": c.name,
                "credits": c.credits,
                "students": [{"id": s.id, "name": s.name} for s in c.students],
                "instructor": (
                    {"id": c.instructor.id, "name": c.instructor.name}
                    if c.instructor
                    else None
                ),
            }
        )
    return jsonify({
        "courses": result,
        "total": total,
        "pages": total_pages,
        "current_page": page
    }), 200


@course_bp.route("/<int:course_id>", methods=["GET"])
@jwt_required()
@role_required("student", "admin", "instructor")
def get_course(course_id):
    course = db_session.get(Course, course_id)
    if not course:
        abort(404, description="Course not found")
    return (
        jsonify(
            {
                "id": course.id,
                "name": course.name,
                "credits": course.credits,
                "students": [{"id": s.id, "name": s.name} for s in course.students],
                "instructor": (
                    {"id": course.instructor.id, "name": course.instructor.name}
                    if course.instructor
                    else None
                ),
            }
        ),
        200,
    )


@course_bp.route("", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_course():
    data = request.get_json()
    if (
        not data
        or not data.get("name")
        or "credits" not in data
        or "instructor_id" not in data
    ):
        abort(
            400,
            description="Invalid data: 'name', 'credits', and 'instructor_id' are required",
        )

    instructor_id = data.get("instructor_id")
    instructor = db_session.get(Instructor, instructor_id)
    if not instructor:
        abort(404, description="Instructor not found")

    try:
        new_course = Course(
            name=data["name"],
            credits=data["credits"],
            instructor_id=instructor_id,
        )
        db_session.add(new_course)
        db_session.commit()
        return (
            jsonify(
                {
                    "id": new_course.id,
                    "name": new_course.name,
                    "credits": new_course.credits,
                    "students": [
                        {"id": s.id, "name": s.name} for s in new_course.students
                    ],
                    "instructor": (
                        {
                            "name": new_course.instructor.name,
                            "id": new_course.instructor.id,
                        }
                        if new_course.instructor
                        else None
                    ),
                }
            ),
            201,
        )
    except Exception:
        db_session.rollback()
        abort(500, description="Database error occurred")


@course_bp.route("/<int:course_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_course(course_id):
    course = db_session.get(Course, course_id)
    if not course:
        abort(404, description="Course not found")

    data = request.get_json()
    if (
        not data
        or not data.get("name")
        or "credits" not in data
        or "instructor_id" not in data
    ):
        abort(
            400,
            description="Invalid data: 'name', 'credits', and 'instructor_id' are required",
        )

    try:
        instructor = db_session.get(Instructor, data["instructor_id"])
        if not instructor:
            abort(404, description="Instructor not found")

        course.name = data["name"]
        course.credits = data["credits"]
        course.instructor_id = data["instructor_id"]

        db_session.commit()
        return (
            jsonify(
                {
                    "id": course.id,
                    "name": course.name,
                    "credits": course.credits,
                    "students": [{"id": s.id, "name": s.name} for s in course.students],
                    "instructor": (
                        {"id": course.instructor.id, "name": course.instructor.name}
                        if course.instructor
                        else None
                    ),
                }
            ),
            200,
        )
    except Exception:
        db_session.rollback()
        abort(500, description="Database error occurred")


@course_bp.route("/<int:course_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_course(course_id):
    course = db_session.get(Course, course_id)
    if not course:
        abort(404, description="Course not found")

    try:
        db_session.delete(course)
        db_session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception:
        db_session.rollback()
        abort(500, description="Database error occurred")


@course_bp.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return jsonify(error=e.name, description=e.description), e.code
