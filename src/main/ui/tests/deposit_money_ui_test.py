import pytest

from src.main.configs.config import Config
from src.main.ui.pages.deposit_page import DepositPage


@pytest.mark.ui
class TestDepositMoney:
    @pytest.mark.parametrize("amount", ["100", "100.01"])
    def test_deposit_money_page(self, user_account, user_session, new_page, amount, api_manager):
        DepositPage(new_page).open().fill_deposit_form(user_account.accountNumber, amount).send_deposit_form()

        balance = api_manager.user_steps.get_account_by_account_number(user_account.accountNumber).balance
        assert balance == float(amount), "Balance did not change on BE"

    @pytest.mark.parametrize(("amount", "message"), [
        ("-100", "Please enter a valid amount"),                                                    # negative
        (None, "Please enter a valid amount"),                                                      # empty
        (str(int(Config.get("maxDepositAmount")) + 1), "Please deposit less or equal to 5000"),     # above the limit
    ])
    def test_deposit_invalid_amount(self, user_account, user_session, new_page, amount, message, api_manager):
        DepositPage(new_page).open().fill_deposit_form(user_account.accountNumber, amount).send_deposit_form(message, context_manager=False)

        balance = api_manager.user_steps.get_account_by_account_number(user_account.accountNumber).balance
        assert balance == 0.0, "Balance changed on BE"

    def test_deposit_no_account(self, user_session, new_page):
        DepositPage(new_page).open().fill_deposit_form(None, "100").send_deposit_form("Please select an account", context_manager=False)
