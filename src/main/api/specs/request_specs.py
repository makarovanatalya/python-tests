import logging

import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest


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
        return {
            'headers': RequestSpecs.default_req_headers(),
            'base_url': Config.get('backendUrl'),
        }

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = 'Basic YWRtaW46YWRtaW4='
        return {
            'headers': headers,
            'base_url': Config.get('backendUrl'),
        }

    @staticmethod
    def user_auth_spec(username: str, password: str):
        auth_url = f'{Config.get('backendUrl')}/auth/login'

        login_user_request = LoginUserRequest(username=username, password=password)
        response = requests.post(url=auth_url, json=login_user_request.model_dump())

        if response.status_code == 200:
            headers = RequestSpecs.default_req_headers()
            headers['Authorization'] = response.headers.get('Authorization')
            return {
                'headers': headers,
                'base_url': Config.get('backendUrl'),
            }
        logging.error(f'Auth failed for {username} with status {response.status_code}: {response.text}')
        raise Exception('Auth failed')
