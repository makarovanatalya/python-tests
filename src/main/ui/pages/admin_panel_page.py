from playwright.sync_api import Page

from src.main.ui.elements.user_bage_element import UserBadgeElement
from src.main.ui.pages.base_page import BasePage


class AdminPanelPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = self.page.locator("text='Admin Panel'")
        self.add_user_button = self.page.locator("text='Add User'")
        self.user_elements = self.page.locator('*:has-text("All Users")').locator('li')

    @property
    def url(self):
        return "/admin"

    def create_user(self, username: str, password: str):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.add_user_button.click()
        return self

    def get_users(self):
        return self.get_page_elements(self.user_elements, UserBadgeElement)

    def find_user_by_username(self, username: str):
        user = [user for user in self.get_users() if user.username == username]
        return user[0] if user else None
