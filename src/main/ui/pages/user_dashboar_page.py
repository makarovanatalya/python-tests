from src.main.ui.pages.base_page import BasePage
from playwright.sync_api import Page


class UserDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = self.page.locator("text='User Dashboard'")
        self.welcome_text = self.page.locator(".welcome-text")
        self.create_account_button = self.page.get_by_role("button", name="Create New Account")

    @property
    def url(self):
        return "/dashboard"