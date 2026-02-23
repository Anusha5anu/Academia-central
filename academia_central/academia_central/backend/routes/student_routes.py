from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from backend.db import students_col, users_col
from bson import ObjectId
from datetime import datetime

student_bp = Blueprint("students", __name__)


def serialize(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


@student_bp.route("/profile", methods=["POST"])
@jwt_required()
def create_profile():
    claims = get_jwt()
    data   = request.get_json()

    profile = {
        "user_id":      claims["sub"],
        "name":         data.get("name"),
        "dob":          data.get("dob"),
        "gender":       data.get("gender"),
        "phone":        data.get("phone"),
        "address":      data.get("address"),
        "department":   data.get("department"),
        "year":         data.get("year"),
        "gpa":          data.get("gpa", 0.0),
        "achievements": data.get("achievements", []),
        "documents":    data.get("documents", []),
        "created_at":   datetime.utcnow()
    }

    if students_col.find_one({"user_id": claims["sub"]}):
        return jsonify({"error": "Profile already exists. Use PUT to update."}), 409

    result = students_col.insert_one(profile)
    return jsonify({"message": "Profile created!", "id": str(result.inserted_id)}), 201


@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_my_profile():
    claims  = get_jwt()
    profile = students_col.find_one({"user_id": claims["sub"]})

    if not profile:
        return jsonify({"error": "Profile not found. Please create one first."}), 404

    return jsonify(serialize(profile)), 200


@student_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    claims = get_jwt()
    data   = request.get_json()
    students_col.update_one({"user_id": claims["sub"]}, {"$set": data})
    return jsonify({"message": "Profile updated!"}), 200


@student_bp.route("/search", methods=["GET"])
@jwt_required()
def search_students():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    name   = request.args.get("name", "").strip()
    dept   = request.args.get("department", "").strip()
    year   = request.args.get("year", "").strip()
    gpa    = request.args.get("gpa", "").strip()

    # ── Strategy: search users collection first by name, then merge profile data ──
    # This way students show up even if they haven't filled in their profile yet.

    results = []

    if name and not dept and not year and not gpa:
        # Name-only search: check BOTH users (registered) and students (profile) collections

        # 1. Find matching users by name (case-insensitive)
        matching_users = list(users_col.find(
            {"name": {"$regex": name, "$options": "i"}, "role": "student"}
        ))

        for u in matching_users:
            uid = str(u["_id"])
            # Try to get their profile details
            profile = students_col.find_one({"user_id": uid})
            if profile:
                profile["_id"] = str(profile["_id"])
                results.append(profile)
            else:
                # No profile yet — show basic info from users collection
                results.append({
                    "_id":        uid,
                    "user_id":    uid,
                    "name":       u.get("name", "—"),
                    "email":      u.get("email", "—"),
                    "department": "Not set",
                    "year":       "Not set",
                    "gpa":        "Not set",
                    "phone":      "Not set",
                    "note":       "Profile not created yet"
                })

        # Also search students collection by name in case name differs
        profile_matches = list(students_col.find(
            {"name": {"$regex": name, "$options": "i"}}
        ))
        existing_ids = {r["user_id"] for r in results}
        for p in profile_matches:
            if p.get("user_id") not in existing_ids:
                p["_id"] = str(p["_id"])
                results.append(p)

    else:
        # Department / year / GPA filter — search profiles collection
        query = {}
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if dept:
            query["department"] = dept
        if year:
            query["year"] = int(year)
        if gpa:
            query["gpa"] = {"$gte": float(gpa)}

        results = list(students_col.find(query))
        for r in results:
            r["_id"] = str(r["_id"])

    return jsonify(results), 200


@student_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_students():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    # Merge users + profiles so ALL registered students appear
    all_users = list(users_col.find({"role": "student"}))
    results   = []

    for u in all_users:
        uid     = str(u["_id"])
        profile = students_col.find_one({"user_id": uid})
        if profile:
            profile["_id"] = str(profile["_id"])
            results.append(profile)
        else:
            results.append({
                "_id":        uid,
                "user_id":    uid,
                "name":       u.get("name", "—"),
                "email":      u.get("email", "—"),
                "department": "—",
                "year":       "—",
                "gpa":        "—",
                "phone":      "—"
            })

    return jsonify(results), 200