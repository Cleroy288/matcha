from flask import request, jsonify
from services.auth_service import register_user, login_user
from utils.jwt_required import jwt_required


def register():

	data = request.json
	
	try:  
		user_id = register_user(
			data["email"],
			data["username"],
			data["password"],
			data["first_name"],
			data["last_name"]
		)

		return jsonify({"user_id": user_id}), 201

	except Exception as e:
		return jsonify({"error": str(e)}), 400
	
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    try:
        token = login_user(username, password)
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def testmiddleware(payload):
    user_id = payload["user_id"]
    return jsonify({"message": f"Hello user {user_id}"})
