import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user import CreateUserResponse
from src.main.api.models.profile import ProfileRequest


@pytest.mark.api
class TestChangeName:
    @pytest.mark.parametrize("name", ("lalala la", ))
    def test_change_name(self, api_manager: ApiManager, user_request: CreateUserResponse, name: str):
        update_name_request = ProfileRequest(name=name)
        change_name_response = api_manager.user_steps.update_profile(user_request.username, user_request.password, update_name_request)
        assert change_name_response.customer.name == name

        profile = api_manager.user_steps.get_profile(user_request.username, user_request.password)
        assert profile.name == name
