# ── backend/db.py ──────────────────────────────────────────────────────────────
# This file handles the connection to MongoDB.
# We connect once here and reuse the same connection everywhere.

from pymongo import MongoClient
import os

# Read the MongoDB URL from our .env file
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/academia_central")

# Create a MongoClient — this is our "gateway" to the database
client = MongoClient(MONGO_URI)

# Select the database named "academia_central"
db = client["academia_central"]

# ── Collections (like tables in SQL) ──────────────────────────────────────────
# Each collection stores a specific type of document (record).

users_col    = db["users"]      # Stores admin & student login accounts
students_col = db["students"]   # Stores student profiles
courses_col  = db["courses"]    # Stores available courses
enrollments_col = db["enrollments"]  # Stores which student enrolled in which course
