from abc import ABC, abstractmethod
from contextlib import contextmanager

from playwright.sync_api import Page
from typing import Self, TypeVar, Type, List

T = TypeVar('T', bound='BasePage')
E = TypeVar('E', bound='BaseElement')  # noqa: F821

class BasePage(ABC):
    def __init__(self, page: Page):
        self.page = page
        self.current_alert_message = None

        self.username_field = self.page.get_by_placeholder("Username")
        self.password_field = self.page.get_by_placeholder("Password")

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
            assert alert_message in self.current_alert_message
            dialog.value.accept()

    def _handle_dialog(self, dialog):
        """
        uses as alternative for context manager check_alert_message_and_accept,
        in cases when the manager isn't applicable for some reason
        """
        self.current_alert_message = dialog.message
        dialog.dismiss()

    @staticmethod
    def get_page_elements(locator, page_element_class: Type[E]) -> List[E]:
        return [page_element_class(locator) for locator in locator.all()]