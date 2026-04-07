import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY", "replace-with-a-long-random-secret-key-2026-dev"
    )
    API_KEY = os.getenv("API_KEY")

    # File upload configurations
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "static", "uploads", "profile_pics")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB max size
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

