import pytest

from src.main.classes.api_manager import ApiManager
from src.main.api.models.create_user import CreateUserResponse


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self,  api_manager: ApiManager, user_request: CreateUserResponse) -> None :
        api_manager.user_steps.create_account()
