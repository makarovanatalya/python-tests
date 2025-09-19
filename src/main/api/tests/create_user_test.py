import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.debug
    def test_create_user(self) -> None :
        create_user_request = CreateUserRequest(
            username=RandomData.get_username(),
            password=RandomData.get_password(),
            role='USER'
        )

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created(),
        ).post(create_user_request)

        assert create_user_response.username == create_user_request.username
        assert create_user_response.role == create_user_request.role

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted(),
        ).delete(create_user_response.id)


    @pytest.mark.parametrize(
        argnames='username,password,role,error_key,error_value',
        argvalues=[
            ('', RandomData.get_password(), 'USER', 'username', 'Username must be between 3 and 15 characters'),
            ('ab', RandomData.get_password(), 'USER', 'username', 'Username must be between 3 and 15 characters'),
            ('ababababababababababababab', RandomData.get_password(), 'USER', 'username', 'Username must be between 3 and 15 characters'),
            ('@ababab', RandomData.get_password(), 'USER', 'username', 'Username must contain only letters, digits, dashes, underscores, and dots'),

        ]
    )
    def test_create_invalid_user(self, username: str, password: str, role: str, error_key: str, error_value: str) -> None:
        create_user_request = CreateUserRequest(username=username, password=password, role=role)

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_bad_request(error_key, error_value),
        ).post(create_user_request)
