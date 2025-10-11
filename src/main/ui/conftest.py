from typing import Any, Generator

import pytest
from playwright.sync_api import Page, Browser, BrowserContext

from src.main.configs.config import Config
from src.main.api.models.create_user import CreateUserRequest
from src.main.ui.helpers.context import add_item_to_local_storage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": Config.get("ui_base_url"),
    }

@pytest.fixture
def new_context(browser: Browser, browser_context_args) -> BrowserContext:
    return browser.new_context(**browser_context_args)

@pytest.fixture
def new_page(new_context) -> Generator[Page, Any, None]:
    yield new_context.new_page()


@pytest.fixture
def admin_session(new_context, api_manager):
    add_item_to_local_storage(
        context=new_context,
        item_key="authToken",
        item_value=api_manager.user_steps.set_user(CreateUserRequest.get_admin()).get_auth_token()
)

@pytest.fixture
def user_session(new_context, api_manager, user_request):
    add_item_to_local_storage(
        context=new_context,
        item_key="authToken",
        item_value=api_manager.user_steps.set_user(user_request).get_auth_token()
)
