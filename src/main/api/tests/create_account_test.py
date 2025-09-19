import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateAccount:
    @pytest.mark.parametrize(
        argnames='username, password, role',
        argvalues=[
            (RandomData.get_username(), RandomData.get_password(), 'USER'),
        ]

    )
    def test_create_account(self,  username: str, password: str, role: str) -> None :
        create_user_request = CreateUserRequest(username=username, password=password, role=role)

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created(),
        ).post(create_user_request)

        login_user_request = LoginUserRequest(username=username, password=password)

        login_user_response = LoginUserRequester(
            RequestSpecs.unauth_spec(),
            ResponseSpecs.request_returns_ok(),
        ).post(login_user_request)

        assert login_user_response.username == create_user_request.username
        assert login_user_response.role == create_user_request.role


        create_account_response = CreateAccountRequester(
            RequestSpecs.user_auth_spec(create_user_request.username, create_user_request.password),
            ResponseSpecs.entity_was_created(),
        ).post()

        assert create_account_response.balance == 0.0
        assert not create_account_response.transactions


        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted(),
        ).delete(create_user_response.id)


