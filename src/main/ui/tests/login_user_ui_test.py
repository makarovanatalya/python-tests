import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user import CreateUserRequest


@pytest.mark.ui
class TestLoginUser:
    def test_login_admin(self, new_page):
        new_page.goto("/login")

        new_page.get_by_placeholder("Username").fill("admin")
        new_page.get_by_placeholder("Password").fill("admin")
        new_page.click('button:has-text("Login")')

        admin_panel_header = new_page.locator("text='Admin Panel'")
        admin_panel_header.wait_for(state="visible")

    def test_login_user(self, new_page, api_manager: ApiManager):
        user = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user)

        new_page.goto("/login")

        new_page.get_by_placeholder("Username").fill(user.username)
        new_page.get_by_placeholder("Password").fill(user.password)
        new_page.click('button:has-text("Login")')

        user_panel_header = new_page.locator("text='User Dashboard'")
        user_panel_header.wait_for(state="visible")

        welcome_text = new_page.locator(".welcome-text")
        welcome_text.wait_for(state="visible")
        assert welcome_text.text_content() == "Welcome, noname!"
