from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
import requests
from playwright.sync_api import Browser, Page, sync_playwright

from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER, AUTH_URL
from niffler_e_2_e_tests_python.fixtures.database import db_niffler_auth  # noqa F401
from niffler_e_2_e_tests_python.presentation.registration.register_page import RegisterPage

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.fixtures.database import DB


@pytest.fixture(scope='class')
def prepare_test_user(db_niffler_auth: 'DB'):
    """Создаем тестового юзера."""
    number_of_users: str = db_niffler_auth.get_value(
        'select count(*) from "user" where username = \'%s\'' % TEST_USER,
    )[0][0]
    if not bool(number_of_users):
        cookie: str = '; '.join((
            requests.get(AUTH_URL).history[0].headers['Set-Cookie'].replace(', ', '').split(
                '; Path=/',
            )[:2]
        ))
        response = requests.post(
            f'{AUTH_URL}{RegisterPage.path}',
            data=dict(
                _csrf=cookie.split('; ')[0].split('XSRF-TOKEN=')[1],
                username=TEST_USER,
                password=TEST_PASSWORD,
                passwordSubmit=TEST_PASSWORD,
            ),
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie}
        )
        # тут, как я понял на запросе происходит редирект, который делает запросом GET
        assert len(response.history) == 0
        assert response.history[0].status_code == HTTPStatus.FOUND
        assert response.history[0].text == ''


@pytest.fixture(scope='session')
def driver() -> Page:
    """Получить WebDriver."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(channel="chrome", headless=False)
        page: Page = browser.new_page()
        yield page
        page.close()
        browser.close()
