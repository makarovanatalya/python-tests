import pytest

from src.main.api.generators.random_data import RandomData
from src.main.classes.api_manager import ApiManager
from src.main.ui.pages.edit_profile_page import EditProfilePage


@pytest.mark.ui
class TestChangeName:
    def test_user_can_change_name(self, new_context, new_page, api_manager: ApiManager, user_session):
        name = RandomData.get_name()
        EditProfilePage(new_page).open().change_name(name).check_name_is(name)

        assert api_manager.user_steps.get_profile().name == name, "Name did not change on BE"

    def test_user_can_not_change_name_to_invalid(self, new_context, new_page, api_manager: ApiManager, user_session):
        EditProfilePage(new_page).open().change_name(
            RandomData.get_faker().last_name(),
            "Name must contain two words with letters only"
        ).check_name_is("Noname")

        assert not api_manager.user_steps.get_profile().name, "Name changed on BE"