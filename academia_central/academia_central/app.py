# ── app.py ─────────────────────────────────────────────────────────────────────
# This is the main entry point of our Flask web application.
# Flask is a lightweight Python web framework that makes it easy to build websites.

from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load variables from our .env file (keeps secrets out of code)
load_dotenv()

# ── Import all our route "blueprints" ─────────────────────────────────────────
# A Blueprint is like a mini-app that handles a specific section of the website.
from backend.routes.auth_routes import auth_bp
from backend.routes.student_routes import student_bp
from backend.routes.course_routes import course_bp
from backend.routes.admin_routes import admin_bp
from backend.routes.page_routes import page_bp

def create_app():
    """Create and configure the Flask application."""

    # __name__ tells Flask where to look for templates and static files
    app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

    # ── Configuration ──────────────────────────────────────────────────────────
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # ── Initialize JWT (JSON Web Token) for login sessions ────────────────────
    JWTManager(app)

    # ── Register all Blueprints (route groups) ────────────────────────────────
    app.register_blueprint(page_bp)          # HTML page rendering
    app.register_blueprint(auth_bp,    url_prefix="/api/auth")     # /api/auth/login etc.
    app.register_blueprint(student_bp, url_prefix="/api/students") # /api/students/...
    app.register_blueprint(course_bp,  url_prefix="/api/courses")  # /api/courses/...
    app.register_blueprint(admin_bp,   url_prefix="/api/admin")    # /api/admin/...

    return app


# ── Run the app ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    # debug=True means Flask will auto-restart when you change code
    app.run(debug=True, port=5000)
