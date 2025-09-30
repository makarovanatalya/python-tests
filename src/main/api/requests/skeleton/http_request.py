from typing import Protocol, Callable

from requests import Request

from src.main.api.requests.skeleton.endpoint import Endpoint


class HTTPRequest(Protocol):
    def __init__(self, endpoint: Endpoint, request_spec: Request, response_spec: Callable):
        self.endpoint = endpoint
        self.request_spec = request_spec
        self.response_spec = response_spec