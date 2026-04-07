from flask import Blueprint, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from app.models.instructor import Instructor
from app.models.user import User
from database import db_session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import role_required

instructor_bp = Blueprint("instructors", __name__)


@instructor_bp.route("", methods=["GET"])
@jwt_required()
@role_required("admin", "student", "instructor")
def get_all_instructors():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search_query = request.args.get("q", "", type=str)

    query = Instructor.query
    if search_query:
        query = query.filter(Instructor.name.ilike(f"%{search_query}%"))

    total = query.count()
    import math
    total_pages = math.ceil(total / per_page)

    instructors = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for instructor in instructors:
        result.append(
            {
                "id": instructor.id,
                "name": instructor.name,
                "major": instructor.major,
                "user_id": instructor.user_id,
            }
        )
    return jsonify({
        "instructors": result,
        "total": total,
        "pages": total_pages,
        "current_page": page
    }), 200


@instructor_bp.route("/me", methods=["GET"])
@jwt_required()
@role_required("instructor")
def get_my_profile():
    user_id = get_jwt_identity()
    instructor = Instructor.query.filter_by(user_id=user_id).first()
    if not instructor:
        abort(404, description="Instructor profile not found")

    return (jsonify({"id": instructor.id,
                     "name": instructor.name,
                     "major": instructor.major,
                     "user_id": instructor.user_id,
                     "courses": [{"id": c.id,
                                  "name": c.name,
                                  "credits": c.credits,
                                  "students": [
                                      {"id": s.id} for s in c.students
                                  ]} for c in instructor.courses],
                     }),
            200,
            )


@instructor_bp.route("/<int:instructor_id>", methods=["GET"])
@jwt_required()
@role_required("admin", "student", "instructor")
def get_instructor(instructor_id):
    instructor = db_session.get(Instructor, instructor_id)
    if not instructor:
        abort(404, description="Instructor not found")

    return (
        jsonify(
            {
                "id": instructor.id,
                "name": instructor.name,
                "major": instructor.major,
                "user_id": instructor.user_id,
            }
        ),
        200,
    )


@instructor_bp.route("", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_instructor():
    data = request.get_json()
    if (
        not data
        or not data.get("name")
        or not data.get("major")
        or "user_id" not in data
    ):
        abort(
            400,
            description="Invalid data: 'name', 'major', and 'user_id' are required",
        )

    user = db_session.get(User, data["user_id"])
    if not user:
        abort(404, description="User not found")

    existing_instructor = Instructor.query.filter_by(user_id=data["user_id"]).first()
    if existing_instructor:
        abort(400, description="An instructor already exists for this user_id")

    try:
        new_instructor = Instructor(
            name=data["name"], major=data["major"], user_id=data["user_id"]
        )
        db_session.add(new_instructor)
        db_session.commit()

        return (
            jsonify(
                {
                    "id": new_instructor.id,
                    "name": new_instructor.name,
                    "major": new_instructor.major,
                    "user_id": new_instructor.user_id,
                }
            ),
            201,
        )
    except Exception:
        db_session.rollback()
        abort(500, description="Database error occurred")


@instructor_bp.route("/<int:instructor_id>", methods=["PUT"])
@jwt_required()
@role_required("admin")
def update_instructor(instructor_id):
    instructor = db_session.get(Instructor, instructor_id)
    if not instructor:
        abort(404, description="Instructor not found")

    data = request.get_json()
    if not data or not data.get("name") or not data.get("major"):
        abort(400, description="Invalid data: 'name' and 'major' are required")

    try:
        instructor.name = data["name"]
        instructor.major = data["major"]

        if "user_id" in data:
            user = db_session.get(User, data["user_id"])
            if not user:
                abort(404, description="User not found")

            existing_instructor = Instructor.query.filter_by(
                user_id=data["user_id"]
            ).first()
            if existing_instructor and existing_instructor.id != instructor.id:
                abort(400, description="An instructor already exists for this user_id")

            instructor.user_id = data["user_id"]

        db_session.commit()
        return (
            jsonify(
                {
                    "id": instructor.id,
                    "name": instructor.name,
                    "major": instructor.major,
                    "user_id": instructor.user_id,
                }
            ),
            200,
        )
    except Exception:
        db_session.rollback()
        abort(500, description="Database error occurred")


@instructor_bp.route("/<int:instructor_id>", methods=["DELETE"])
@jwt_required()
@role_required("admin")
def delete_instructor(instructor_id):
    instructor = db_session.get(Instructor, instructor_id)
    if not instructor:
        abort(404, description="Instructor not found")

    try:
        db_session.delete(instructor)
        db_session.commit()
        return jsonify({"message": "Instructor deleted successfully"}), 200
    except Exception:
        db_session.rollback()
        abort(500, description="Database error occurred")


@instructor_bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=e.name, description=e.description), e.code
