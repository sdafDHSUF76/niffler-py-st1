from typing import TYPE_CHECKING, Callable, Optional

import pytest
import requests

from niffler_e_2_e_tests_python.configs import FRONT_URL1, TEST_USER, TEST_PASSWORD, GATEWAY_URL
from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from niffler_e_2_e_tests_python.fixtures.database import DB
    from playwright.sync_api import Page
    from _pytest.fixtures import SubRequest
    from _pytest.mark import Mark

    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.fixture(scope='class')
def main_page(driver: 'Page') -> MainPage:
    """Получаем страницу Main со всей логикой ее."""
    return MainPage(driver)

@pytest.fixture
def create_spends(get_token: Callable[[str, str], str], request: 'SubRequest'):
    """Создаем категории через API.

    На самом деле тут только через API категория создается, а вот токен берется из UI.
    """
    marker: Optional['Mark'] = request.node.get_closest_marker('spend_data')
    user_old, password_old = None, None
    for unit in marker.args:
        user, password = unit['user'], unit['password']
        if user_old != user and password_old != password:
            token: str = get_token(unit['user'], unit['password'])
        requests.post(
            f'{GATEWAY_URL}/api/spends/add',
            json=unit['spend'],
            headers={
                'Authorization': token,
                'Content-Type': 'application/json',
            }
        )
        user_old, password_old = user, password

@pytest.fixture
def goto_main(login_page: 'LoginPage', main_page: 'MainPage', presentation_page: 'PresentationPage'):
    if (
        main_page.driver.locator(main_page.main).is_visible()
        and main_page.driver.url != f'{FRONT_URL1}/main'
    ):
        main_page.click(main_page.main)
    if presentation_page.driver.url != f'{FRONT_URL1}/main':
        presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)
        login_page.authorization(TEST_USER, TEST_PASSWORD)
    if main_page.driver.locator(main_page.main).is_hidden() and presentation_page.driver.url == f'{FRONT_URL1}/main':
        # presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)
        login_page.authorization(TEST_USER, TEST_PASSWORD)


@pytest.fixture
def reload_main(main_page: 'MainPage'):
    if (
        main_page.driver.locator(main_page.main).is_visible()
        and main_page.driver.url == f'{FRONT_URL1}/main'
    ):
        main_page.driver.reload()