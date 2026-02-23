# ── backend/routes/auth_routes.py ─────────────────────────────────────────────
# Handles user Registration and Login.
# Passwords are hashed (scrambled) with bcrypt so they are never stored as plain text.

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from backend.db import users_col
from datetime import datetime
import bcrypt

# Create a Blueprint named "auth"
auth_bp = Blueprint("auth", __name__)


# ── REGISTER ──────────────────────────────────────────────────────────────────
# Route: POST /api/auth/register
# Anyone can call this to create a new account.
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()  # Get the JSON body sent by the frontend

    # Basic validation — make sure required fields are present
    required = ["name", "email", "password", "role"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Check if the email is already used
    if users_col.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already registered"}), 409

    # Hash the password — NEVER store plain passwords
    hashed_pw = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    # Build the user document to insert into MongoDB
    user = {
        "name":       data["name"],
        "email":      data["email"],
        "password":   hashed_pw,          # Stored as bytes
        "role":       data["role"],        # "student" or "admin"
        "created_at": datetime.utcnow()
    }

    users_col.insert_one(user)
    return jsonify({"message": "Account created successfully!"}), 201


# ── LOGIN ──────────────────────────────────────────────────────────────────────
# Route: POST /api/auth/login
# Returns a JWT token if credentials are correct.
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Find the user by email
    user = users_col.find_one({"email": data.get("email")})

    # Check if user exists AND the password matches the stored hash
    if not user or not bcrypt.checkpw(data.get("password", "").encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create a JWT token. The "identity" is stored inside the token.
    # additional_claims lets us attach extra info like role.
    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={"role": user["role"], "name": user["name"]}
    )

    return jsonify({
        "token": token,
        "role":  user["role"],
        "name":  user["name"]
    }), 200
