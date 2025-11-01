from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Self, TypeVar, Type, List

from playwright.sync_api import Page

from src.main.ui.elements.account_option_element import AccountOption

T = TypeVar('T', bound='BasePage')
E = TypeVar('E', bound='BaseElement')  # noqa: F821

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.current_alert_message = None
        self.expected_alert_message = None
        self._alert_button = None

        self.username_field = self.page.get_by_placeholder("Username")
        self.password_field = self.page.get_by_placeholder("Password")

        self.account_selector = self.page.locator(".account-selector")
        self.account_options = self.account_selector.locator("option")

        self.name = self.page.locator(".user-name")

    @property
    @abstractmethod
    def url(self): ...

    def open(self) -> Self:
        self.page.goto(self.url)
        return self

    def get_page(self, page_class: Type[T]) -> T:
        return page_class(self.page)

    @contextmanager
    def check_alert_message_and_accept(self, alert_message: str):
        with self.page.expect_event("dialog") as dialog:
            yield
            self.current_alert_message = dialog.value.message
            assert alert_message in self.current_alert_message, f"Incorrect error message: {self.current_alert_message}"
            dialog.value.accept()

    def _handle_dialog(self, dialog):
        self.current_alert_message = dialog.message
        dialog.dismiss()

    # workaround: for incorrect deposit click doesn't work with context manager
    def handle_alert_and_check_message(self, error_message):
        """
        uses as alternative for context manager check_alert_message_and_accept,
        in cases when the manager isn't applicable for some reason
        SET self._alert_button before using!
        """
        self.page.once("dialog", self._handle_dialog)
        self._alert_button.click()
        assert error_message in self.current_alert_message, f"Incorrect error message: {self.current_alert_message}"
        return self

    @staticmethod
    def get_page_elements(locator, page_element_class: Type[E]) -> List[E]:
        return [page_element_class(locator) for locator in locator.all()]

    def check_name_is(self, name: str):
        self.page.reload()
        self.name.wait_for(state="visible")
        assert self.name.text_content() == name, "Name is incorrect"
        return self

    def _get_account_options(self):
        self.account_options.first.wait_for(state="attached")
        return self.get_page_elements(self.account_options, AccountOption)

    def _get_account_by_number(self, account_number):
        self.account_options.filter(has_text=account_number) .wait_for(state="attached") # wait for needed account number
        account = [acc for acc in self._get_account_options() if acc.account_number == account_number]
        return account[0] if account else None

    def select_account_by_number(self, account_number: str):
        if account_number:
            account = self._get_account_by_number(account_number)
            assert account, f"Could not find account with number {account_number}"
            self.account_selector.select_option(value=account.value)
        return self
