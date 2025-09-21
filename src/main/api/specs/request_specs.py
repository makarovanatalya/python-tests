import requests

DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


class RequestSpecs:
    @staticmethod
    def unauth_spec():
        return requests.Request(headers=DEFAULT_HEADERS)

    @staticmethod
    def _auth_spec(username: str, password: str):
        return requests.Request(headers=DEFAULT_HEADERS, auth=(username, password))

    @staticmethod
    def admin_auth_spec():
        return RequestSpecs._auth_spec('admin', 'admin')

    @staticmethod
    def user_auth_spec(username: str, password: str):
        return RequestSpecs._auth_spec(username, password)
