import logging

import requests

from src.main.api.configs.config import Config
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.crud_requester import CrudRequester
from src.main.api.specs.response_specs import ResponseSpecs


class RequestSpecs:
    BASE_URL = 'http://localhost:4111/api/v1'

    @staticmethod
    def default_req_headers():
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @staticmethod
    def unauth_spec():
        return RequestSpecs.default_req_headers()

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = 'Basic YWRtaW46YWRtaW4='
        return headers

    @staticmethod
    def user_auth_spec(username: str, password: str):
        try:
            response = CrudRequester(
                Endpoint.LOGIN_USER,
                RequestSpecs.unauth_spec(),
                ResponseSpecs.request_returns_ok()
            ).post(LoginUserRequest(username=username, password=password))
            headers = RequestSpecs.default_req_headers()
            headers['Authorization'] = response.headers.get('Authorization')
            return headers
        except Exception as e:
            logging.error(f'Auth failed for {username} with error: {e}')
            raise Exception('Auth failed')
