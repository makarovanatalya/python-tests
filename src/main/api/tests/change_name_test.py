import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user import CreateUserResponse
from src.main.api.models.profile import ProfileRequest


@pytest.mark.api
class TestChangeName:
    @pytest.mark.parametrize("name", (RandomData.get_faker().name() , ))
    def test_change_name(self, api_manager: ApiManager, user_request: CreateUserResponse, name: str):
        update_name_request = ProfileRequest(name=name)
        change_name_response = api_manager.user_steps.update_profile(update_name_request)
        assert change_name_response.customer.name == name

        profile = api_manager.user_steps.get_profile()
        assert profile.name == name

    @pytest.mark.parametrize(
        "name",
        [
            "",                                                                             #empty
            RandomData.get_faker().last_name(),                                             # only first/last name
            RandomData.get_faker().name() + RandomData.get_random_special_symbol(),         # with special symbol
            f"{RandomData.get_faker().name()}{RandomData.get_faker().random_digit()}",      # with number
            f"{RandomData.get_faker().name()} {RandomData.get_faker().first_name()}",       # 3 words
            RandomData.get_faker().random_letter()*100,                                     # too long
        ]
    )
    def test_change_name_to_invalid(
            self, api_manager: ApiManager, user_request: CreateUserResponse, name: str
    ):
        error_text = "Name must contain two words with letters only"
        update_name_request = ProfileRequest(name=name)
        api_manager.user_steps.update_profile_with_invalid_data(update_name_request, error_text)