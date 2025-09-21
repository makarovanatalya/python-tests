from http import HTTPMethod
from typing import TypeVar, Optional

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HTTPRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface

T = TypeVar('T', bound=BaseModel)

class CrudRequester(HTTPRequest, CrudEndpointInterface):
    def _send_request(self, method: HTTPMethod, endpoint: str, body: str) -> requests.Response:
        self.request_spec.url = f"{Config.get('server')}{Config.get('api_version')}{self.endpoint.value.url}{endpoint}"
        self.request_spec.method = method
        self.request_spec.json = body

        with requests.Session() as session:
            return session.send(session.prepare_request(self.request_spec))

    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model else ""
        return self._send_request(HTTPMethod.POST, endpoint="", body=body)

    def get(self, model: BaseModel, id: int): ...

    def update(self, model: BaseModel, id: int): ...

    def delete(self, id: int) -> requests.Response:
        return self._send_request(HTTPMethod.POST, endpoint=f"/{id}", body="")
