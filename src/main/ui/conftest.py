from typing import Any, Generator

import pytest
from playwright.sync_api import Page, Browser, BrowserContext

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    base_url = "http://localhost:3000"  # TODO: get from env

    return {
        **browser_context_args,
        "base_url": base_url,
    }


@pytest.fixture(scope="function")
def new_context(browser: Browser, browser_context_args) -> Generator[BrowserContext, Any, None]:
    yield browser.new_context(**browser_context_args)

@pytest.fixture(scope="function")
def new_page(new_context) -> Generator[Page, Any, None]:
    yield new_context.new_page()