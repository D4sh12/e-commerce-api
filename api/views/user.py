""" Module for users endpoints """

from flask import request
from flask_restx import Resource
import bcrypt
import random
import string
from api.utilities.helpers import request_data_strip
from api.utilities.helpers.swagger.collections import user_namespace
from api.utilities.helpers.swagger.models.user import (
    signup_model,
    login_model,
    reset_request_model,
    reset_password_model,
    confirm_code_request_model,
    resend_code_request_model,
)
from api.utilities.helpers.responses import success_response, error_response
from api.utilities.validators.user import UserValidators
from api.utilities.generate_token import generate_auth_token, verify_user_token
from api.utilities.send_email import send_email
from api.models.user import User
from api.models.cart import Cart
from api.schemas.user import UserSchema


@user_namespace.route("/signup")
class UserSignupResource(Resource):
    """ " Resource class for user signup endpoint"""

    @user_namespace.expect(signup_model)
    def post(self):
        """Endpoint to create the user"""

        request_data = request.get_json()
        UserValidators.validate(request_data)

        request_data = request_data_strip(request_data)

        bytes_password = bytes(request_data["password"], encoding="utf-8")
        hashed = bcrypt.hashpw(bytes_password, bcrypt.gensalt(10))
        request_data["password"] = hashed.decode("utf-8")

        confirmation_code = "".join(random.choices(string.digits, k=6))
        request_data["confirmation_code"] = confirmation_code

        new_user = User(**request_data)
        new_user.save()

        user_schema = UserSchema()
        user_data = user_schema.dump(new_user)

        send_email(user_data, "Confirmation Email", "confirmation_email.html")

        return {
            "status": "success",
            "message": "User successfully created. Please check your email to continue.",
        }, 201


@user_namespace.route("/activate/<string:token>")
class UserActivateResource(Resource):
    """ " Resource class for user account activation endpoint"""

    def get(self, token):
        """Endpoint to activate the user account"""

        user = verify_user_token(token)
        if user is None:
            error_response["message"] = "Account activation token is invalid"
            return error_response, 400

        if user.is_activated:
            error_response["message"] = "User account already activated"
            return error_response, 400

        user.update({"is_activated": True})
        user_cart = Cart(user_id=user.id)
        user_cart.save()

        return {"status": "success", "message": "User successfully activated"}, 200


@user_namespace.route("/login")
class UserLoginResource(Resource):
    """ " Resource class for user login endpoint"""

    @user_namespace.expect(login_model)
    def post(self):
        """Endpoint to login the user"""

        request_data = request.get_json()
        email = request_data["email"]
        password = bytes(request_data["password"], encoding="utf-8")
        user: User = User.query.filter(User.email == email).first()
        error_response["message"] = "Incorrect username or password"
        user_schema = UserSchema()

        if user:
            if not user.is_activated:
                error_response["message"] = "Your account has not yet been verified"
                return error_response, 434

            user_data = user_schema.dump(user)
            hashed = bytes(user_data["password"], encoding="utf-8")

            if bcrypt.checkpw(password, hashed):
                user_schema = UserSchema(exclude=["password"])
                logged_in_user = user_schema.dump(user)
                token = generate_auth_token(logged_in_user)
                success_response["message"] = "User successfully logged in"
                success_response["data"] = {"token": token, "user": logged_in_user}

                return success_response, 200
            return error_response, 404
        return error_response, 404


@user_namespace.route("/reset-password")
class ResetRequestResource(Resource):
    """ Resource class for user password reset request"""

    @user_namespace.expect(reset_request_model)
    def post(self):
        """Endpoint to request password reset code"""

        request_data = request.get_json()
        email = request_data["email"]
        user = User.find_by_email(email)

        if not user:
            error_response["message"] = "User not found"
            return error_response, 404

        reset_code = ''.join(random.choices(string.digits, k=6))
        user.update({"reset_code": reset_code})

        user_schema = UserSchema()
        send_email(
            user_schema.dump(user),
            "Password Reset Request",
            "password_reset_email.html",
        )

        return {
            "status": "success",
            "message": "Request successfully submitted. Please check your email to continue.",
        }, 200


@user_namespace.route("/reset-password/verify-code")
class PasswordResetVerifyCodeResource(Resource):
    """ Resource class for verifying reset code and changing password """

    @user_namespace.expect(reset_password_model)
    def post(self):
        """Endpoint to verify reset code and change the user password"""

        request_data = request.get_json()
        email = request_data.get("email")
        reset_code = request_data.get("reset_code")
        new_password = request_data.get("new_password")

        user = User.query.filter_by(email=email).first()

        if user is None or user.reset_code != reset_code:
            error_response["message"] = "Invalid reset code"
            return error_response, 400

        UserValidators.validate_password(new_password)
        bytes_password = bytes(new_password, encoding="utf-8")
        hashed = bcrypt.hashpw(bytes_password, bcrypt.gensalt(10))
        password = hashed.decode("utf-8")

        user.update({"password": password, "reset_code": None})

        return {
            "status": "success",
            "message": "User password successfully changed",
        }, 200


@user_namespace.route("/verify-code")
class UserVerifyCodeResource(Resource):
    """Resource class for user account verification via confirmation code"""
    
    @user_namespace.expect(confirm_code_request_model)
    def post(self):
        """Endpoint to verify the user account via confirmation code"""

        request_data = request.get_json()
        email = request_data.get("email")
        confirmation_code = request_data.get("confirmation_code")

        user = User.query.filter_by(email=email).first()

        if user.is_activated:
            error_response["message"] = "User account already activated"
            return error_response, 400

        if user is None or user.confirmation_code != confirmation_code:
            error_response["message"] = "Invalid confirmation code"
            return error_response, 400


        user.update({"is_activated": True, "confirmation_code": None})
        user_cart = Cart(user_id=user.id)
        user_cart.save()

        return {"status": "success", "message": "User successfully activated"}, 200


@user_namespace.route("/resend-code")
class ResendCodeResource(Resource):
    """Resource class for resending the confirmation code"""

    @user_namespace.expect(resend_code_request_model)
    def post(self):
        """Endpoint to resend the confirmation code"""

        request_data = request.get_json()
        email = request_data.get("email")

        user = User.query.filter_by(email=email).first()

        if user is None:
            error_response["message"] = "User not found"
            return error_response, 404

        if user.is_activated:
            error_response["message"] = "User account already activated"
            return error_response, 400

        confirmation_code = "".join(random.choices(string.digits, k=6))
        user.update({"confirmation_code": confirmation_code})

        user_schema = UserSchema()
        user_data = user_schema.dump(user)

        send_email(user_data, "Confirmation Email", "confirmation_email.html")

        return {
            "status": "success",
            "message": "Confirmation code successfully resent. Please check your email to continue.",
        }, 200
