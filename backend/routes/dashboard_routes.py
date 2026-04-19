from flask import Blueprint


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard/<int:hospital_id>", methods=["GET"])
def dashboard(hospital_id):
    try:
        pass
    except Exception as e:
        pass
