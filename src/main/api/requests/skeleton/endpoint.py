from dataclasses import dataclass
from enum import Enum

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserRequest, CreateUserResponse
from src.main.api.models.login_user import LoginUserRequest, LoginUserResponse

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