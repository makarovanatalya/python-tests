from dataclasses import dataclass
from enum import Enum

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: BaseModel
    response_model: BaseModel

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfig(
        url='/admin/users',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
    )

    ADMIN_DELETE_USER = EndpointConfig(
        url='/admin/users',
        request_model=None,
        response_model=None,
    )

    LOGIN_USER = EndpointConfig(
        url='/auth/login',
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
    )

    CREATE_ACCOUNT = EndpointConfig(
        url='/accounts',
        request_model=None,
        response_model=CreateAccountResponse,
    )