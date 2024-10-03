import pytest
from playwright.sync_api import Browser, Page, sync_playwright


@pytest.fixture(scope='session')
def driver() -> Page:
    """Получить WebDriver."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(channel="chrome", headless=False)
        page: Page = browser.new_page()
        yield page
        page.close()
        browser.close()
