from flask import request, jsonify, make_response
from services.auth_service import register_user, login_user, reset_password_user, verify_reset_password_user, verify_email_user, email_verification_disabled
from utils.jwt_required import jwt_required
from models.user_model import get_user_by_id
from utils.constants import AuthMessages
from controllers.constants import HTTP_OK, HTTP_CREATED, HTTP_BAD_REQUEST, HTTP_NOT_FOUND

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

		message = AuthMessages.REGISTER_SUCCESS_NO_EMAIL if email_verification_disabled() else AuthMessages.REGISTER_SUCCES
		return jsonify({"message": message}), HTTP_CREATED

	except Exception as e:
		return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
	
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    try:
        token, user_data = login_user(username, password)
        
        response = make_response(jsonify({
            "message": AuthMessages.LOGIN_SUCCESS,
            "user": user_data
        }), HTTP_OK)

        response.set_cookie(
            "auth_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600
        )

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
    
def logout():
    response = make_response(jsonify({"message": "Logged out"}), HTTP_OK)
    response.delete_cookie("auth_token")
    return response
    
def verify_email():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": AuthMessages.NOT_TOKEN}), HTTP_BAD_REQUEST

    try:
        verify_email_user(token)
        return jsonify({"message": AuthMessages.EMAIL_VERIFIED}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
    
def verify_reset_password():
    data = request.json
    password = data["password"]
    token = request.args.get('token')
    if not token:
        return jsonify({"error": AuthMessages.NOT_TOKEN}), HTTP_BAD_REQUEST

    try:
        verify_reset_password_user(token, password)
        return jsonify({"message": AuthMessages.PASSWORD_RESET_OK}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

def reset_password():
    data = request.json
    email = data["email"]
    if not email:
         return jsonify({"error": AuthMessages.NOT_EMAIL}), HTTP_BAD_REQUEST

    try:
        reset_password_user(email)
        return jsonify({"message": AuthMessages.EMAIL_SEND_SUCCESS}), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

# TEST ca va disparaitre
@jwt_required # A mettre au dessus d'un controller pour proteger sa route
def testmiddleware(payload): 
    user_id = payload["user_id"]
    user = get_user_by_id(user_id) 
    
    if not user:
        return jsonify({"error": AuthMessages.USER_NOT_FOUND}), HTTP_NOT_FOUND
        
    return jsonify({
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    })
