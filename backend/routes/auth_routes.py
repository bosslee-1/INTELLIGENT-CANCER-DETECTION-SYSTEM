from flask import Blueprint

from controllers.auth_controller import login_user, register_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    print("✅ auth routes loaded")
    return register_user()


@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user()


# similar to this
"""
router.post("/register", registerUser)
"""
