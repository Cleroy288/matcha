from flask import request, jsonify
from services.auth_service import register_user, login_user, reset_password_user, verify_reset_password_user, verify_email_user
from utils.jwt_required import jwt_required
from models.user_model import get_user_by_id


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
        token, user_data = login_user(username, password)
        return jsonify({
            "token": token,
            "user": user_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def verify_email():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token manquant"}), 400

    try:
        verify_email_user(token)
        return jsonify({"message": "Email vérifié avec succès ! Tu peux maintenant te connecter."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
def verify_reset_password():
    data = request.json
    password = data["password"]
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token manquant"}), 400

    try:
        verify_reset_password_user(token, password)
        return jsonify({"message": "Mot de passe modifié avec succès ! Tu peux maintenant te connecter."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def reset_password():
    data = request.json
    email = data["email"]
    if not email:
         return jsonify({"error": "email manquante"}), 400

    try:
        reset_password_user(email)
        return jsonify({"message": "Email envoyé avec succès ! Tu peux maintenant clic sur le lien dans ton mail pour changer de mot de passe."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# TEST ca va disparaitre
@jwt_required # A mettre au dessus d'un controller pour proteger sa route
def testmiddleware(payload): 
    user_id = payload["user_id"]
    user = get_user_by_id(user_id) 
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    })
