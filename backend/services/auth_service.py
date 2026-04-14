from flask import jsonify
from config.supabase_client import supabase
import hashlib

def login_user(data):
    try:
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        hashed = hashlib.sha256(password.encode()).hexdigest()

        res = supabase.table("users").select("*").eq("email", email).execute()

        if not res.data:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

        user = res.data[0]

        if user["password_hash"] != hashed:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401

        return jsonify({"success": True, "user": user}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500