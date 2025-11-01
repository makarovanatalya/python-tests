import allure
from playwright.sync_api import Page

from src.main.ui.helpers import screenshot
from src.main.ui.pages.base_page import BasePage


class TransferPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.recipient_name = self.page.get_by_placeholder("Enter recipient name")
        self.recipient_account_number = self.page.get_by_placeholder("Enter recipient account number")
        self.amount = self.page.get_by_placeholder("Enter amount")
        self.checkbox = self.page.get_by_role("checkbox", name="Confirm details are correct")
        self.send_transfer_button = self.page.locator('button:has-text("Send Transfer")')

    @property
    def url(self):
        return "/transfer"

    def fill_transfer_form(self, account_number, recipient_name, recipient_account_number, amount, checkbox=True, message: str = None):
        with allure.step("fill transfer form"):
            self.select_account_by_number(account_number)
            if recipient_name:
                self.recipient_name.fill(recipient_name)
            if recipient_account_number:
                self.recipient_account_number.fill(recipient_account_number)
            if amount:
                self.amount.fill(amount)
            if checkbox:
                self.checkbox.check()

            self.expected_alert_message = f"Successfully transferred ${amount} to account {recipient_account_number}!"
            screenshot.attach_page_screenshot(self.page, "fill_transfer_form")
        return self

    def send_transfer_form(self, message: str = None, context_manager=True):
        with allure.step("send transfer form"):
            message = message or self.expected_alert_message
            if context_manager:
                with self.check_alert_message_and_accept(message):
                    self.send_transfer_button.click()
            else:
                self._alert_button = self.send_transfer_button
                self.handle_alert_and_check_message(message)
            screenshot.attach_page_screenshot(self.page, "send_transfer_form")
        return self

