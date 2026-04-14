from flask import Blueprint, request, jsonify
import hashlib
import datetime
import random

# create blueprint
auth_bp = Blueprint("auth", __name__)

# You will import supabase from app later
from app import supabase


# ============================
# REGISTER ROUTE
# ============================
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        hospital = data.get("hospital", {})
        admin = data.get("admin", {})
        security = data.get("security", {})

        # hash password
        password_hash = hashlib.sha256(
            security.get("password", "").encode()
        ).hexdigest()

        # ============================
        # 1. Insert Hospital
        # ============================
        hospital_res = supabase.table("hospitals").insert({
            "name": hospital.get("name"),
            "email": hospital.get("email"),
            "phone": hospital.get("phone"),
            "address": hospital.get("address"),
            "city": hospital.get("city"),
            "state": hospital.get("state"),
            "postal_code": hospital.get("postal_code"),
            "country": hospital.get("country"),
            "type": hospital.get("type"),
            "created_at": datetime.datetime.utcnow().isoformat()
        }).execute()

        if not hospital_res.data:
            return jsonify({"success": False, "error": "Hospital creation failed"}), 400

        hospital_id = hospital_res.data[0]["id"]

        # ============================
        # 2. Insert User (Admin)
        # ============================
        user_res = supabase.table("users").insert({
            "hospital_id": hospital_id,
            "full_name": admin.get("fullName"),
            "email": admin.get("email"),
            "password_hash": password_hash,
            "role": "super_admin",
            "department": admin.get("department"),
            "phone": admin.get("phone"),
            "created_at": datetime.datetime.utcnow().isoformat()
        }).execute()

        if not user_res.data:
            return jsonify({"success": False, "error": "User creation failed"}), 400

        return jsonify({
            "success": True,
            "message": "Registration successful"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500