from http import HTTPStatus
from typing import TypeVar, Optional, Union

import requests

from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HTTPRequest
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface


T = TypeVar('T', bound=BaseModel)

class CrudRequester(HTTPRequest, CrudEndpointInterface):
    def post(self, model: Optional[T] = None) -> requests.Response:
        body = model.model_dump() if model else ""
        response = requests.post(
            url = f"{Config.get('server')}{Config.get('api_version')}{self.endpoint.value.url}",
            headers = self.request_spec,
            json=body,
        )
        self.response_spec(response)
        return response

    def get(self, id: int): ...

    def update(self, model: BaseModel, id: int): ...

    def delete(self, id: int) -> requests.Response:
        response = requests.delete(
            url=f"{Config.get('server')}{Config.get('api_version')}{self.endpoint.value.url}/{id}",
            headers=self.request_spec,
        )
        self.response_spec(response)
        return response
