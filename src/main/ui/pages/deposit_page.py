from playwright.sync_api import Page

from src.main.ui.elements.account_option_element import AccountOption
from src.main.ui.pages.base_page import BasePage


class DepositPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.account_selector = self.page.locator(".account-selector")
        self.account_options = self.account_selector.locator("option")
        self.deposit_input = self.page.locator(".deposit-input")
        self.deposit_button = self.page.locator('button:has-text("Deposit")')

        self.__account_number = None
        self.__amount = None

    @property
    def url(self):
        return "/deposit"

    def _get_account_options(self):
        self.account_options.first.wait_for(state="attached")
        return self.get_page_elements(self.account_options, AccountOption)

    def _get_account_by_number(self, account_number):
        self.account_options.filter(has_text=account_number)  # check for needed account number
        account = [acc for acc in self._get_account_options() if acc.account_number == account_number]
        return account[0] if account else None

    def fill_deposit_form(self, account_number: str = None, amount: str = None):
        if account_number:
            account = self._get_account_by_number(account_number)
            assert account, f"Could not find account with number {account_number}"
            self.account_selector.select_option(value=account.value)
            self.__account_number = account_number
        if amount:
            self.deposit_input.fill(amount)
            self.__amount = amount
        return self

    def send_deposit_form_success(self):
        with self.check_alert_message_and_accept(f"Successfully deposited ${self.__amount} to account {self.__account_number}!"):
            self.deposit_button.click()
        return self

    # workaround: for incorrect deposit click doesn't work with context manager
    def send_deposit_form_failure(self, error_message):
        self.page.once("dialog", self._handle_dialog)
        self.deposit_button.click()
        assert error_message in self.current_alert_message, "Incorrect error message"
        return self
