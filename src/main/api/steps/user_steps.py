from typing import List, Any

from requests import Response

from src.main.api.models.account import GetAccountsResponse, Account
from src.main.api.models.comparasion.model_assertions import ModelAssertions
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.deposit_money import DepositMoneyResponse, DepositMoneyRequest
from src.main.api.models.login_user import LoginUserRequest, LoginUserResponse
from src.main.api.models.profile import ProfileRequest, ProfileResponse, Profile
from src.main.api.models.transfer import TransferResponse, TransferRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.crud_requester import CrudRequester
from src.main.api.requests.skeleton.requester.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def __init__(self, created_object: List[Any]):
        super().__init__(created_object)
        self.user = None

    def set_user(self, user: CreateUserRequest):
        self.user = user
        return self

    @staticmethod
    def _user_must_be_set(func):
        def wrapper(self, *args, **kwargs):
            assert self.user is not None, "User must be set before calling this step"
            return func(self, *args, **kwargs)
        return wrapper

    @_user_must_be_set
    def login(self) -> LoginUserResponse:
        login_request = LoginUserRequest(username=self.user.username, password=self.user.password)
        login_response: LoginUserResponse = ValidatedCrudRequester(
            endpoint=Endpoint.LOGIN_USER,
            request_spec=RequestSpecs.unauth_spec(),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).post(login_request)
        ModelAssertions(self.user, login_response).match()
        return login_response

    @_user_must_be_set
    def create_account(self) -> CreateAccountResponse:
        create_account_response: CreateAccountResponse = ValidatedCrudRequester(
            endpoint=Endpoint.CREATE_ACCOUNT,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).post(LoginUserRequest(username=self.user.username, password=self.user.password))

        assert create_account_response.balance == 0.0
        assert not create_account_response.transactions
        return create_account_response

    @_user_must_be_set
    def deposit_money(self, account_id: int, amount: float) -> DepositMoneyResponse:
        deposit_money_request: DepositMoneyRequest = DepositMoneyRequest(id=account_id, balance=amount)
        deposit_money_response: DepositMoneyResponse = ValidatedCrudRequester(
            endpoint=Endpoint.DEPOSIT_MONEY,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).post(model=deposit_money_request)
        ModelAssertions(deposit_money_request, deposit_money_response).match()
        return deposit_money_response

    @_user_must_be_set
    def deposit_money_incorrectly(self, account_id: int, amount: float, error_text: str) -> Response:
        deposit_money_request: DepositMoneyRequest = DepositMoneyRequest(id=account_id, balance=amount)
        return CrudRequester(
            endpoint=Endpoint.DEPOSIT_MONEY,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_error(error_text),
        ).post(model=deposit_money_request)

    @_user_must_be_set
    def transfer_money(self, sender_account_id: int, receiver_account_id: int, amount: float) -> TransferResponse:
        transfer_response: TransferResponse = ValidatedCrudRequester(
            endpoint=Endpoint.TRANSFER,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).post(model=TransferRequest(senderAccountId=sender_account_id, receiverAccountId=receiver_account_id, amount=amount))

        assert transfer_response.amount == amount
        assert transfer_response.message == "Transfer successful"

        return transfer_response

    @_user_must_be_set
    def transfer_money_incorrectly(self, sender_account_id: int, receiver_account_id: int, amount: float, error_text: str) -> Response:
        return CrudRequester(
            endpoint=Endpoint.TRANSFER,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_error(error_text),
        ).post(model=TransferRequest(senderAccountId=sender_account_id, receiverAccountId=receiver_account_id, amount=amount))

    @_user_must_be_set
    def get_profile(self) -> Profile:
        return ValidatedCrudRequester(
            endpoint=Endpoint.GET_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).get()

    @_user_must_be_set
    def update_profile(self, update_profile_request: ProfileRequest) -> ProfileResponse:
        return ValidatedCrudRequester(
            endpoint=Endpoint.UPDATE_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).update(update_profile_request)

    @_user_must_be_set
    def update_profile_with_invalid_data(self, update_profile_request: ProfileRequest, error_text: str) -> Response:
        return CrudRequester(
            endpoint=Endpoint.UPDATE_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_error(error_text),
        ).update(update_profile_request)

    @_user_must_be_set
    def get_accounts(self) -> GetAccountsResponse:
        return ValidatedCrudRequester(
            endpoint=Endpoint.GET_ACCOUNTS,
            request_spec=RequestSpecs.user_auth_spec(self.user.username, self.user.password),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).get()

    @_user_must_be_set
    def get_account_by_id(self, account_id: int) -> Account:
        accounts = self.get_accounts()
        account = [acc for acc in accounts.root if acc.id == account_id]
        assert len(account) == 1, f"Could not find account with id {account_id}"
        return account[0]
