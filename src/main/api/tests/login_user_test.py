import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_requests import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse


@pytest.mark.api
class TestLoginUser:
    def test_login_user(self, api_manager: ApiManager, user_request: CreateUserResponse) -> None :
        api_manager.user_steps.login(user_request)

    def test_login_admin_user(self, api_manager: ApiManager) -> None :
        api_manager.user_steps.login(CreateUserRequest(username='admin', password='admin', role='ADMIN'))
