from flask import jsonify, request

from backend.database.user_queries import register_user_query



def register_user():
    try:
        data = request.get_json()
        result = register_user_query(data)
        if result["success"]:
            return jsonify(result),201
        else:
            return jsonify(result),400
        
    except Exception as e:
        return jsonify({
            "success":False,
            "error":str(e)
        }),500
    

'''

The above is similar to this in nodejs

# export const registerUser = async (req, res) => {
#    const result = await createUser(req.body)
# }


'''