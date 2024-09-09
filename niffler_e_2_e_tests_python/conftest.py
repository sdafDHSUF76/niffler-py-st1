from typing import TYPE_CHECKING

import pytest
from _pytest.fixtures import SubRequest
from allure_commons.reporter import AllureReporter
from fixtures.conftest import db_niffler_auth  # noqa F401
from playwright.sync_api import Browser, Page, sync_playwright

if TYPE_CHECKING:
    from _pytest.config import PytestPluginManager
    from pytest import FixtureDef


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: 'FixtureDef', request: SubRequest):
    yield
    # Очищаем из тега allure упоминание о usefixtures
    if len(request.node.own_markers):
        [
            request.node.own_markers.pop(i) for i, value in enumerate(request.node.own_markers)
            if value.name == 'usefixtures'
        ]
    # добавляем в к тексту allure обозначения scope у фикстур setup, teardown
    plugins: 'PytestPluginManager' = request.config.pluginmanager
    if plugins.has_plugin('allure_listener'):
        logger: AllureReporter = plugins.get_plugin('allure_listener').allure_logger
        item = logger.get_last_item()
        scope_letter = fixturedef.scope[0].upper()
        item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()
    # TODO сделать так и для teardown, а то у них нету буквы


@pytest.fixture(scope='session')
def driver() -> Page:
    """Получить WebDriver."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(channel="chrome", headless=False)
        page: Page = browser.new_page()
        yield page
        page.close()
        browser.close()
