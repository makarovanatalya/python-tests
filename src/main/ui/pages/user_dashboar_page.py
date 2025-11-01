import re

import allure
from playwright.sync_api import Page

from src.main.ui.helpers import screenshot
from src.main.ui.pages.base_page import BasePage


class UserDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = self.page.locator("text='User Dashboard'")
        self.welcome_text = self.page.locator(".welcome-text")
        self.create_account_button = self.page.get_by_role("button", name="Create New Account")

    @property
    def url(self):
        return "/dashboard"

    def create_account(self):
        with allure.step("create account"):
            with self.check_alert_message_and_accept("Account Created!"):
                self.create_account_button.click()
            screenshot.attach_page_screenshot(self.page, "create_account")
        return self

    @allure.step
    def create_account_and_get_account_number(self):
        self.create_account()
        account_number = None
        match = re.search(r"Account Number: (\w+)", self.current_alert_message)
        if match:
            account_number = match.group(1)
        assert account_number, "Could not extract account number"
        return account_number
