from flask import Blueprint, render_template, redirect, url_for

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    return redirect(url_for("web.login"))


@web_bp.route("/login")
def login():
    return render_template("public/login.html")


@web_bp.route("/register")
def register():
    return render_template("public/register.html")

# --- Admin Routes ---


@web_bp.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")


@web_bp.route("/admin/students")
def admin_students():
    return render_template("admin/students.html")


@web_bp.route("/admin/instructors")
def admin_instructors():
    return render_template("admin/instructors.html")


@web_bp.route("/admin/add-user")
def admin_add_user():
    return render_template("admin/add_user.html")


@web_bp.route("/admin/courses")
def admin_courses():
    return render_template("admin/courses.html")

# --- Instructor Routes ---


@web_bp.route("/instructor/dashboard")
def instructor_dashboard():
    return render_template("instructor/dashboard.html")


@web_bp.route("/instructor/courses")
def instructor_courses():
    return render_template("instructor/courses.html")

# --- Student Routes ---


@web_bp.route("/student/dashboard")
def student_dashboard():
    return render_template("student/dashboard.html")


@web_bp.route("/student/my-courses")
def student_my_courses():
    return render_template("student/my_courses.html")


@web_bp.route("/student/catalog")
def student_catalog():
    return render_template("student/catalog.html")


@web_bp.route("/course/<int:course_id>")
def course_details(course_id):
    return render_template("shared/course_details.html", course_id=course_id)
