""" Module for testing reset user password endpoints """

import time
from flask import json
from tests.constants import API_BASE_URL, CONTENT_TYPE
from tests.mocks.user import (
    RESET_REQUEST_USER, UNEXISTED_RESET_REQUEST_USER, RESET_PASSWORD_NEW_PASSWORD)
import api.views.user
from api.utilities.generate_token import generate_user_token


class TestPasswordResetEndpoints:
    """ Class for testing user password reset resources """

    def test_reset_request_succeeds(self, client, init_db, new_activated_user):
        """ Testing reset request """

        new_activated_user.save()
        user_data = json.dumps(RESET_REQUEST_USER)
        response = client.post(
            f'{API_BASE_URL}/auth/reset-password', data=user_data, content_type=CONTENT_TYPE)
        message = 'Request successfully submitted. Please check your email to continue.'

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == message

    def test_reset_request_with_unexisted_user_fails(self, client, init_db):
        """ Testing reset request with unexisted user """

        user_data = json.dumps(UNEXISTED_RESET_REQUEST_USER)
        response = client.post(
            f'{API_BASE_URL}/auth/reset-password', data=user_data, content_type=CONTENT_TYPE)
        message = 'User not found'

        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['message'] == message

    def test_reset_password_succeeds(self, client, init_db, new_activated_user):
        """ Testing reset password """

        new_activated_user.save()
        reset_code = new_activated_user.reset_code
        user_data = json.dumps({
            "email": new_activated_user.email,
            "reset_code": reset_code,
            "new_password": RESET_PASSWORD_NEW_PASSWORD["password"]
        })

        response = client.post(
            f'{API_BASE_URL}/auth/reset-password/verify-code',
            data=user_data, content_type=CONTENT_TYPE)
        message = 'User password successfully changed'

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['message'] == message

    def test_reset_password_with_invalid_code_fails(self, client, init_db, new_activated_user):
        """ Testing reset password with invalid code """

        new_activated_user.save()
        user_data = json.dumps({
            "email": new_activated_user.email,
            "reset_code": "123456",
            "new_password": RESET_PASSWORD_NEW_PASSWORD["password"]
        })

        response = client.post(
            f'{API_BASE_URL}/auth/reset-password/verify-code',
            data=user_data, content_type=CONTENT_TYPE)
        message = 'Invalid reset code'

        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['message'] == message
