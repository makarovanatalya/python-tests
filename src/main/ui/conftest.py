import logging
from typing import Any, Generator

import pytest
from playwright.sync_api import Page, Browser, BrowserContext

from src.main.api.configs.config import Config


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": Config.get("ui_base_url"),
    }


@pytest.fixture(scope="function")
def new_context(browser: Browser, browser_context_args) -> BrowserContext:
    return browser.new_context(**browser_context_args)


@pytest.fixture(scope="function")
def local_storage():
    """
    returns dict where key = local storage item name and value = local storage item value
    use with context_with_local_storage to have prepared local storage itn tests (e.g. for authorization)
    """
    return {}

@pytest.fixture(scope="function", autouse=True)
def context_with_local_storage(new_context, local_storage):
    if not local_storage:
        logging.debug("No local storage was set for the test")
        return
    for key, value in local_storage.items():
        script = f"window.localStorage.setItem('{key}', '{value}');"
        new_context.add_init_script(script)


@pytest.fixture(scope="function")
def new_page(new_context) -> Generator[Page, Any, None]:
    yield new_context.new_page()