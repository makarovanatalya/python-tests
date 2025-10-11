import pytest
from playwright.sync_api import expect

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest


@pytest.mark.ui
class TestCreateUser:

    def test_admin_can_create_user(self, new_context, new_page,  api_manager: ApiManager):
        auth_token = api_manager.user_steps.set_user(CreateUserRequest(username="admin", password="admin", role="ADMIN")).get_auth_token()
        script = "window.localStorage.setItem('authToken', '" + auth_token + "');"
        new_context.add_init_script(script)

        new_page.goto("/admin")
        admin_panel_header = new_page.locator("text='Admin Panel'")
        admin_panel_header.wait_for(state="visible")

        new_user : CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_page.get_by_placeholder("Username").fill(new_user.username)
        new_page.get_by_placeholder("Password").fill(new_user.password)

        add_user = new_page.locator("text='Add User'")
        add_user.wait_for(state="visible")

        with new_page.expect_event("dialog") as dialog:
            add_user.click()
            assert "User created successfully!" in dialog.value.message
            dialog.value.accept()

        users = new_page.locator('*:has-text("All Users")').locator('li')
        user = users.filter(has_text=f"{new_user.username}USER")
        user.wait_for(state="visible")

        users = api_manager.admin_steps.get_users()
        created_user = [user for user in users if user.username == new_user.username]
        assert created_user, "User was not created on BE"

    def test_admin_can_not_create_user_with_invalid_data(self, new_context, new_page,  api_manager: ApiManager):
        auth_token = api_manager.user_steps.set_user(CreateUserRequest(username="admin", password="admin", role="ADMIN")).get_auth_token()
        script = "window.localStorage.setItem('authToken', '" + auth_token + "');"
        new_context.add_init_script(script)

        new_page.goto("/admin")
        admin_panel_header = new_page.locator("text='Admin Panel'")
        admin_panel_header.wait_for(state="visible")

        new_user: CreateUserRequest = RandomModelGenerator.generate(CreateUserRequest)
        new_user.username = "a"

        new_page.get_by_placeholder("Username").fill(new_user.username)
        new_page.get_by_placeholder("Password").fill(new_user.password)

        add_user = new_page.locator("text='Add User'")
        add_user.wait_for(state="visible")

        with new_page.expect_event("dialog") as dialog:
            add_user.click()
            assert "Failed to create user" in dialog.value.message
            assert " username: Username must be between 3 and 15 characters" in dialog.value.message
            dialog.value.accept()

        users = new_page.locator('*:has-text("All Users")').locator('li')
        user = users.filter(has_text=f"^{new_user.username}\\s?")
        expect(user).to_be_hidden()

        users = api_manager.admin_steps.get_users()
        created_user = [user for user in users if user.username == new_user.username]
        assert not created_user, "User was created on BE"
