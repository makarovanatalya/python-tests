from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Union

from pydantic import RootModel

from src.main.api.models.account import GetAccountsResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserRequest, CreateUserResponse
from src.main.api.models.deposit_money import DepositMoneyRequest, DepositMoneyResponse
from src.main.api.models.login_user import LoginUserRequest, LoginUserResponse
from src.main.api.models.profile import ProfileRequest, ProfileResponse
from src.main.api.models.transfer import TransferRequest, TransferResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Union[Type[BaseModel], Type[RootModel]]]

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

    DEPOSIT_MONEY = EndpointConfig(
        url='/accounts/deposit',
        request_model=DepositMoneyRequest,
        response_model=DepositMoneyResponse,
    )

    GET_ACCOUNTS = EndpointConfig(
        url='/customer/accounts',
        request_model=None,
        response_model=GetAccountsResponse,
    )

    TRANSFER = EndpointConfig(
        url='/accounts/transfer',
        request_model=TransferRequest,
        response_model=TransferResponse,
    )

    GET_PROFILE = EndpointConfig(
        url='/customer/profile',
        request_model=None,
        response_model=ProfileResponse,
    )

    UPDATE_PROFILE = EndpointConfig(
        url='/customer/profile',
        request_model=ProfileRequest,
        response_model=ProfileResponse,
    )
