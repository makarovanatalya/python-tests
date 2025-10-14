import pytest

from src.main.api.models.create_user import CreateUserRequest
from src.main.ui.pages.admin_panel_page import AdminPanelPage
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.user_dashboar_page import UserDashboardPage


@pytest.mark.ui
class TestLoginUser:
    def test_login_admin(self, new_page):
        admin = CreateUserRequest.get_admin()
        admin_panel_page = LoginPage(new_page).open().login(admin.username, admin.password).get_page(AdminPanelPage)
        admin_panel_page.header.wait_for(state="visible")

    def test_login_user(self, new_page, user_request):
        user_dashboard = LoginPage(new_page).open().login(user_request.username, user_request.password).get_page(UserDashboardPage)
        user_dashboard.header.wait_for(state="visible")
        user_dashboard.welcome_text.wait_for(state="visible")
        assert user_dashboard.welcome_text.text_content() == "Welcome, noname!"
