from flask import Blueprint


auth_bp = Blueprint("auth", __name__)
@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user()



# similar to this 
'''
router.post("/register", registerUser)
'''
