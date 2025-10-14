from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage


class EditProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.name_field = self.page.get_by_placeholder("Enter new name")
        self.save_changes_button = self.page.locator('button:has-text("Save Changes")')

    @property
    def url(self):
        return "/edit-profile"

    def change_name(self, name, message="Name updated successfully!"):
        with self.check_alert_message_and_accept(message):
            self.name_field.fill(name)
            self.save_changes_button.click()
        return self
