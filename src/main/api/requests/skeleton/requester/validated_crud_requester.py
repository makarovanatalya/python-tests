from typing import TypeVar, Optional

from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HTTPRequest
from src.main.api.requests.skeleton.requester.crud_requester import CrudRequester

T = TypeVar('T', bound=BaseModel)

class ValidatedCrudRequester(HTTPRequest):
    def __init__(self, endpoint, request_spec, response_spec):
        super().__init__(endpoint, request_spec, response_spec)
        self.crud_requester = CrudRequester(endpoint, request_spec, response_spec)

    def post(self, model: Optional[T]):
        response = self.crud_requester.post(model)
        return self.endpoint.value.response_model.model_validate(response.json())

    def get(self, id: int = None):
        response = self.crud_requester.get(id)
        return self.endpoint.value.response_model.model_validate(response.json())

    def update(self, model: BaseModel, id: int = None):
        response = self.crud_requester.update(model, id)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, id: int): ...
