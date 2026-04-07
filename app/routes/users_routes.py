import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, abort, current_app
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.utils import role_required
from database import db_session

user_bp = Blueprint("users", __name__)


def allowed_file(filename):
    allowed_exts = current_app.config.get("ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "gif"})
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_exts


@user_bp.route("/profile_pic", methods=["POST"])
@jwt_required()
def upload_profile_pic():
    user_id = get_jwt_identity()
    user = db_session.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    if "file" not in request.files:
        abort(400, description="No file part in the request")

    file = request.files["file"]
    if file.filename == "":
        abort(400, description="No selected file")

    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal
        original_filename = secure_filename(file.filename)
        # Create a unique filename to prevent overwriting
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        # Ensure directory exists
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        # Save relative URL to database
        # Assuming static folder is /static/...
        profile_pic_url = f"/static/uploads/profile_pics/{unique_filename}"
        user.profile_pic_url = profile_pic_url
        db_session.commit()

        return jsonify({
            "message": "Profile picture uploaded successfully",
            "profile_pic_url": profile_pic_url
        }), 200

    abort(400, description="Invalid file type. Allowed types are png, jpg, jpeg, gif.")


@user_bp.route("/pending", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_pending_users():
    users = User.query.filter_by(is_active=False).all()
    result = []
    for u in users:
        data = {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at.isoformat() if u.created_at else None
        }
        if u.role == "student" and u.student:
            data["name"] = u.student.name
        elif u.role == "instructor" and u.instructor:
            data["name"] = u.instructor.name
        result.append(data)

    return jsonify(result), 200


@user_bp.route("/<int:user_id>/approve", methods=["POST", "PUT"])
@jwt_required()
@role_required("admin")
def approve_user(user_id):
    user = db_session.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    user.is_active = True
    db_session.commit()

    return jsonify({"message": f"User {user.username} has been approved."}), 200


@user_bp.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=e.name, description=e.description), e.code
