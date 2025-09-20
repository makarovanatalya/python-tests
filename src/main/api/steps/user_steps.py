from src.main.api.models.comparasion.model_assertions import ModelAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
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
