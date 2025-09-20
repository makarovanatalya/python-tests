import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_requests import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self,  api_manager: ApiManager, user_request: CreateUserRequest) -> None :
        api_manager.user_steps.create_account(user_request)
