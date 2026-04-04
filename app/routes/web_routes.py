from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def index():
    return render_template("home.html")

@web_bp.route("/login")
def login():
    return render_template("login.html")

@web_bp.route("/register")
def register():
    return render_template("register.html")

@web_bp.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@web_bp.route("/student")
def student_dashboard():
    return render_template("student_dashboard.html")

@web_bp.route("/course/<int:course_id>")
def course_details(course_id):
    # Renders the template, passing the ID safely via Jinja so JS can grab it or we pull it from URL
    return render_template("course_details.html", course_id=course_id)
