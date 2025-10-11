import pytest

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest
from src.main.classes.api_manager import ApiManager
from src.main.ui.pages.admin_panel_page import AdminPanelPage


@pytest.mark.ui
class TestCreateUser:
    def test_admin_can_create_user(self, new_context, new_page, api_manager: ApiManager, admin_session):
        new_user = RandomModelGenerator.generate(CreateUserRequest)
        admin_page = AdminPanelPage(new_page).open()

        with admin_page.check_alert_message_and_accept("User created successfully!"):
            admin_page.create_user(new_user.username, new_user.password)
        ui_user = admin_page.find_user_by_username(new_user.username)
        assert ui_user, "Could not find user in UI"
        assert ui_user.role == new_user.role, "Role does not match"

        user = api_manager.admin_steps.get_user_by_username(new_user.username)
        assert user, "User was not created on BE"
        api_manager.admin_steps.add_created_object(user)  # to delete it on cleanup

    def test_admin_can_not_create_user_with_invalid_data(self, new_context, new_page,  api_manager: ApiManager, admin_session):
        new_user = RandomModelGenerator.generate(CreateUserRequest)
        new_user.username = "a"
        admin_page = AdminPanelPage(new_page).open()

        with admin_page.check_alert_message_and_accept("Failed to create user"):
            admin_page.create_user(new_user.username, new_user.password)
        ui_user = admin_page.find_user_by_username(new_user.username)
        assert not ui_user, "Found user in UI"

        user = api_manager.admin_steps.get_user_by_username(new_user.username)
        assert not user, "User was created on BE"