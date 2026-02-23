# ── backend/routes/course_routes.py ───────────────────────────────────────────
# Handles Courses: listing, creating (admin), and enrolling (student).

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from backend.db import courses_col, enrollments_col, students_col
from bson import ObjectId
from datetime import datetime

course_bp = Blueprint("courses", __name__)


def serialize(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


# ── LIST ALL COURSES ──────────────────────────────────────────────────────────
# Route: GET /api/courses/
# Any logged-in user can see available courses.
@course_bp.route("/", methods=["GET"])
@jwt_required()
def list_courses():
    courses = list(courses_col.find())
    return jsonify([serialize(c) for c in courses]), 200


# ── CREATE A COURSE (Admin only) ──────────────────────────────────────────────
# Route: POST /api/courses/
@course_bp.route("/", methods=["POST"])
@jwt_required()
def create_course():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    data = request.get_json()
    course = {
        "code":        data.get("code"),         # e.g., "CS101"
        "name":        data.get("name"),         # e.g., "Intro to Python"
        "department":  data.get("department"),
        "credits":     data.get("credits", 3),
        "capacity":    data.get("capacity", 30), # Max students allowed
        "enrolled":    0,                        # Current enrollment count
        "eligibility": data.get("eligibility", []),  # e.g., ["year>=2", "dept=CS"]
        "created_at":  datetime.utcnow()
    }

    result = courses_col.insert_one(course)
    return jsonify({"message": "Course created!", "id": str(result.inserted_id)}), 201


# ── ENROLL IN A COURSE ────────────────────────────────────────────────────────
# Route: POST /api/courses/<course_id>/enroll
# A student sends their request to join a course.
@course_bp.route("/<course_id>/enroll", methods=["POST"])
@jwt_required()
def enroll(course_id):
    claims = get_jwt()
    user_id = claims["sub"]

    # Find the course by its MongoDB ID
    course = courses_col.find_one({"_id": ObjectId(course_id)})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Check if the course still has seats available
    if course["enrolled"] >= course["capacity"]:
        return jsonify({"error": "Course is full!"}), 400

    # Prevent duplicate enrollment
    already = enrollments_col.find_one({"user_id": user_id, "course_id": course_id})
    if already:
        return jsonify({"error": "Already enrolled in this course"}), 409

    # Save the enrollment record
    enrollments_col.insert_one({
        "user_id":    user_id,
        "course_id":  course_id,
        "course_name": course["name"],
        "status":     "pending",   # Pending admin approval
        "enrolled_at": datetime.utcnow()
    })

    # Increment the enrolled count in the course document
    courses_col.update_one({"_id": ObjectId(course_id)}, {"$inc": {"enrolled": 1}})

    return jsonify({"message": f"Enrollment request sent for '{course['name']}'!"}), 201


# ── MY ENROLLMENTS ────────────────────────────────────────────────────────────
# Route: GET /api/courses/my-enrollments
@course_bp.route("/my-enrollments", methods=["GET"])
@jwt_required()
def my_enrollments():
    user_id = get_jwt()["sub"]
    records = list(enrollments_col.find({"user_id": user_id}))
    return jsonify([serialize(r) for r in records]), 200


# ── APPROVE / REJECT ENROLLMENT (Admin) ───────────────────────────────────────
# Route: PUT /api/courses/enrollment/<enrollment_id>
@course_bp.route("/enrollment/<enrollment_id>", methods=["PUT"])
@jwt_required()
def update_enrollment(enrollment_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    data   = request.get_json()
    status = data.get("status")  # "approved" or "rejected"

    if status not in ["approved", "rejected"]:
        return jsonify({"error": "Status must be 'approved' or 'rejected'"}), 400

    enrollments_col.update_one(
        {"_id": ObjectId(enrollment_id)},
        {"$set": {"status": status}}
    )
    return jsonify({"message": f"Enrollment {status}!"}), 200
