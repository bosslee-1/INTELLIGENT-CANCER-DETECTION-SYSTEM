
from flask import Blueprint, request

from backend.services.auth_service import login_user


auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/auth",methods=["POST"])

def login():
    data = request.get_json()
    return login_user(data)