from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage


class DepositPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.deposit_input = self.page.locator(".deposit-input")
        self.deposit_button = self.page.locator('button:has-text("Deposit")')

    @property
    def url(self):
        return "/deposit"

    def fill_deposit_form(self, account_number: str = None, amount: str = None):
        self.select_account_by_number(account_number)
        if amount:
            self.deposit_input.fill(amount)
        self.expected_alert_message = f"Successfully deposited ${amount} to account {account_number}!"
        return self

    def send_deposit_form(self, message: str = None, context_manager=True):
        message = message or self.expected_alert_message
        if context_manager:
            with self.check_alert_message_and_accept(message):
                self.deposit_button.click()
        else:
            self._alert_button = self.deposit_button
            self.handle_alert_and_check_message(message)
