import pytest

from src.main.classes.api_manager import ApiManager
from src.main.ui.pages.user_dashboar_page import UserDashboardPage


@pytest.mark.ui
class TestCreateAccount:
    def test_user_can_create_account(self, new_context, new_page, api_manager: ApiManager, user_session):
        account_number = UserDashboardPage(new_page).open().create_account_and_get_account_number()
        account = api_manager.user_steps.get_account_by_account_number(account_number)
        assert account, "Could not find new account on BE"
