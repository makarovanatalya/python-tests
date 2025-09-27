from src.main.api.models.account import GetAccountsResponse, Account
from src.main.api.models.comparasion.model_assertions import ModelAssertions
from src.main.api.models.create_account import CreateAccountResponse
from src.main.api.models.create_user import CreateUserRequest
from src.main.api.models.deposit_money import DepositMoneyResponse, DepositMoneyRequest
from src.main.api.models.login_user import LoginUserRequest, LoginUserResponse
from src.main.api.models.profile import ProfileRequest, ProfileResponse, Profile
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requester.validated_crud_requester import ValidatedCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def login(self, user_request: CreateUserRequest) -> LoginUserResponse:
        login_request = LoginUserRequest(username=user_request.username, password=user_request.password)
        login_response: LoginUserResponse = ValidatedCrudRequester(
            endpoint=Endpoint.LOGIN_USER,
            request_spec=RequestSpecs.unauth_spec(),
            response_spec=ResponseSpecs.request_returns_ok(),
        ).post(login_request)
        ModelAssertions(user_request, login_response).match()
        return login_response

    def create_account(self, user_request: CreateUserRequest) -> CreateAccountResponse:
        login_request = LoginUserRequest(username=user_request.username, password=user_request.password)
        create_account_response: CreateAccountResponse = ValidatedCrudRequester(
            endpoint=Endpoint.CREATE_ACCOUNT,
            request_spec=RequestSpecs.user_auth_spec(user_request.username, user_request.password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(login_request)

        assert create_account_response.balance == 0.0
        assert not create_account_response.transactions
        return create_account_response

    def deposit_money(self, username: str, password: str, account_id: int, amount: float) -> DepositMoneyResponse:
        deposit_money_request: DepositMoneyRequest = DepositMoneyRequest(
            id=account_id,
            balance=amount
        )
        deposit_money_response: DepositMoneyResponse = ValidatedCrudRequester(
            endpoint=Endpoint.DEPOSIT_MONEY,
            request_spec=RequestSpecs.user_auth_spec(username, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).post(model=deposit_money_request)
        ModelAssertions(deposit_money_request, deposit_money_response).match()
        return deposit_money_response

    def get_profile(self, username: str, password: str) -> Profile:
        return ValidatedCrudRequester(
            endpoint=Endpoint.GET_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(username, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

    def update_profile(self, username: str, password: str, update_profile_request: ProfileRequest) -> ProfileResponse:
        return ValidatedCrudRequester(
            endpoint=Endpoint.UPDATE_PROFILE,
            request_spec=RequestSpecs.user_auth_spec(username, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).update(update_profile_request)

    def get_accounts(self, username: str, password: str) -> GetAccountsResponse:
        return ValidatedCrudRequester(
            endpoint=Endpoint.GET_ACCOUNTS,
            request_spec=RequestSpecs.user_auth_spec(username, password),
            response_spec=ResponseSpecs.request_returns_ok()
        ).get()

    def get_account_by_id(self, username: str, password: str, account_id: int) -> Account:
        accounts = self.get_accounts(username, password)
        account = [acc for acc in accounts.root if acc.id == account_id]
        assert len(account) == 1, f"Could not find account with id {account_id}"
        return account[0]
