from http import HTTPStatus
from typing import Callable

from requests import Response


class ResponseSpecs():
    @staticmethod
    def request_returns_ok() -> Callable:
        def check(response: Response):
            return response.status_code == HTTPStatus.OK
        return check

    @staticmethod
    def entity_was_created()  -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return check

    @staticmethod
    def entity_was_deleted() -> Callable:
        def check(response: Response):
            assert response.status_code in [HTTPStatus.NO_CONTENT, HTTPStatus.OK], response.text
        return check

    @staticmethod
    def request_returns_bad_request(error_key: str, error_value: str) -> Callable:
        def check(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
            assert error_value in response.json().get(error_key), response.text
        return check

    @staticmethod
    def request_returns_error(error_text: str):
        def check(response: Response):
            assert response.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND], "Not expected status code"
            assert error_text in response.text, f"Wrong response: {response.text}"
        return check
