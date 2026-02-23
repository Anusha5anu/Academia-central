# ── backend/routes/page_routes.py ─────────────────────────────────────────────
# Serves the HTML pages (the actual web pages users see in their browser).

from flask import Blueprint, render_template

page_bp = Blueprint("pages", __name__)

@page_bp.route("/")
def index():
    return render_template("index.html")

@page_bp.route("/login")
def login_page():
    return render_template("login.html")

@page_bp.route("/register")
def register_page():
    return render_template("register.html")

@page_bp.route("/student/dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")

@page_bp.route("/student/profile")
def student_profile():
    return render_template("student_profile.html")

@page_bp.route("/student/courses")
def student_courses():
    return render_template("courses.html")

@page_bp.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")
