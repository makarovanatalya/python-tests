from abc import ABC, abstractmethod
from contextlib import contextmanager

from playwright.sync_api import Page
from typing import Self, TypeVar, Type

T = TypeVar('T', bound='BasePage')

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