import allure
from playwright.sync_api import Page

def attach_page_screenshot(page: Page, name):
    allure.attach(
        page.screenshot(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )