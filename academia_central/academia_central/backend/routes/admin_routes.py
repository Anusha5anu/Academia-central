from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from backend.db import students_col, courses_col, enrollments_col, users_col

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    # Count ALL registered student accounts (updates immediately on register)
    total_students    = users_col.count_documents({"role": "student"})
    total_courses     = courses_col.count_documents({})
    total_enrollments = enrollments_col.count_documents({})
    pending_approvals = enrollments_col.count_documents({"status": "pending"})
    approved_count    = enrollments_col.count_documents({"status": "approved"})
    rejected_count    = enrollments_col.count_documents({"status": "rejected"})

    dept_pipeline = [
        {"$group": {"_id": "$department", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    by_department = list(students_col.aggregate(dept_pipeline))
    by_department = [{"department": d["_id"], "count": d["count"]} for d in by_department]

    year_pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    by_year = list(students_col.aggregate(year_pipeline))
    by_year = [{"year": y["_id"], "count": y["count"]} for y in by_year]

    return jsonify({
        "total_students":    total_students,
        "total_courses":     total_courses,
        "total_enrollments": total_enrollments,
        "pending_approvals": pending_approvals,
        "approved_count":    approved_count,
        "rejected_count":    rejected_count,
        "by_department":     by_department,
        "by_year":           by_year
    }), 200


@admin_bp.route("/pending-enrollments", methods=["GET"])
@jwt_required()
def pending_enrollments():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403
    records = list(enrollments_col.find({"status": "pending"}))
    for r in records:
        r["_id"] = str(r["_id"])
    return jsonify(records), 200


@admin_bp.route("/all-enrollments", methods=["GET"])
@jwt_required()
def all_enrollments():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403
    records = list(enrollments_col.find())
    for r in records:
        r["_id"] = str(r["_id"])
    return jsonify(records), 200