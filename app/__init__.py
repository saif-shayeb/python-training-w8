from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    jwt = JWTManager(app)
    
    from database import init_db, db_session
    init_db()

    from app.routes.students_routes import student_bp
    from app.routes.courses_routes import course_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.web_routes import web_bp
    from app.routes.enrollment_routes import enrollment_bp
    
    app.register_blueprint(student_bp, url_prefix="/api/students")
    app.register_blueprint(course_bp, url_prefix="/api/courses")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(enrollment_bp, url_prefix="/api/enrollments")
    app.register_blueprint(web_bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

