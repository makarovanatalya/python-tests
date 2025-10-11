import re

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.ui.pages.user_dashboar_page import UserDashboardPage


@pytest.fixture(scope="function")
def local_storage(api_manager, user_request):
    return {"authToken": api_manager.user_steps.set_user(user_request).get_auth_token()}

@pytest.mark.ui
class TestCreateAccount:
    def test_user_can_create_account(self, new_context, new_page, api_manager: ApiManager):
        user_dashboard_page = UserDashboardPage(new_page).open()

        with user_dashboard_page.check_alert_message_and_accept("New Account Created! Account Number:"):
            user_dashboard_page.create_account_button.click()

        account_number = None
        match = re.search(r"Account Number: (\w+)", user_dashboard_page.current_alert_message)
        if match:
            account_number = match.group(1)
        assert account_number, "Could not extract account number"

        account = api_manager.user_steps.get_account_by_account_number(account_number)
        assert account, "Could not find new account on BE"
