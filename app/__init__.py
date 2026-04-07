from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    JWTManager(app)

    from database import init_db, db_session

    init_db()

    from app.routes.students_routes import student_bp
    from app.routes.courses_routes import course_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.web_routes import web_bp
    from app.routes.enrollment_routes import enrollment_bp
    from app.routes.instructors_routes import instructor_bp
    from app.routes.users_routes import user_bp

    app.register_blueprint(student_bp, url_prefix="/api/students")
    app.register_blueprint(course_bp, url_prefix="/api/courses")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(enrollment_bp, url_prefix="/api/enrollments")
    app.register_blueprint(instructor_bp, url_prefix="/api/instructors")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(web_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
