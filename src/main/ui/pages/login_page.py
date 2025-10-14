from src.main.ui.pages.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_button = self.page.locator('button:has-text("Login")')


    @property
    def url(self):
        return "/login"

    def login(self, username: str, password: str):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
        return self



