from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from allure_commons.reporter import AllureReporter
from playwright.sync_api import Browser, Page, sync_playwright

from niffler_e_2_e_tests_python.client_api import ClientApi
from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.fixtures.database import db_niffler_auth  # noqa F401
from _pytest.fixtures import SubRequest

if TYPE_CHECKING:
    from _pytest.config import PytestPluginManager
    from pytest import FixtureDef
    from requests import Response

    from niffler_e_2_e_tests_python.fixtures.database import DB


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


@pytest.fixture(scope='session', autouse=True)
def prepare_test_user(db_niffler_auth: 'DB'):
    """Создаем тестового юзера.

    Создаем через базу, если юзер есть, то не создаем.
    """
    number_of_users: int = db_niffler_auth.get_value(
        'select count(*) from "user" where username = \'%s\'' % TEST_USER,
    )[0][0]
    if not number_of_users:
        response: 'Response' = ClientApi().create_user(TEST_USER, TEST_PASSWORD)
        assert len(response.history) == 0
        assert response.status_code == HTTPStatus.CREATED


@pytest.fixture(scope='session')
def driver() -> Page:
    """Получить WebDriver."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(channel="chrome", headless=False)
        page: Page = browser.new_page()
        yield page
        page.close()
        browser.close()
