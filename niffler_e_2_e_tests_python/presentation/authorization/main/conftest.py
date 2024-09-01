from typing import TYPE_CHECKING, Optional

import pytest

from niffler_e_2_e_tests_python.client_api import ClientApi
from niffler_e_2_e_tests_python.configs import FRONT_URL1, TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
from niffler_e_2_e_tests_python.utils import get_join_url

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.mark import Mark
    from playwright.sync_api import Page

    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.fixture(scope='session')
def main_page(driver: 'Page') -> MainPage:
    """Получаем страницу Main со всей логикой ее."""
    return MainPage(driver)


@pytest.fixture
def create_spends(request: 'SubRequest'):
    """Создаем категории через API.

    На самом деле тут только через API категория создается, а вот токен берется из UI.
    """
    marker: Optional['Mark'] = request.node.get_closest_marker('spend_data')
    user_old, password_old = None, None
    for unit in marker.args:
        user, password = unit['user'], unit['password']
        if user_old != user and password_old != password:
            token: str = ClientApi().get_token(unit['user'], unit['password'])
        ClientApi().add_spend(unit['spend'], token)
        user_old, password_old = user, password


@pytest.fixture
def goto_main(
    login_page: 'LoginPage', main_page: 'MainPage', presentation_page: 'PresentationPage',
):
    """Перейти на страницу main из разных мест сайта."""
    if (
        main_page.driver.locator(main_page.main).is_visible()
        and main_page.driver.url != get_join_url(FRONT_URL1, MainPage.path)
    ):
        main_page.click(main_page.main)
    if presentation_page.driver.url != get_join_url(FRONT_URL1, MainPage.path):
        presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)
        login_page.authorization(TEST_USER, TEST_PASSWORD)
    if (
        main_page.driver.locator(main_page.main).is_hidden()
        and presentation_page.driver.url == get_join_url(FRONT_URL1, MainPage.path)
    ):
        presentation_page.click(presentation_page.button_login)
        login_page.authorization(TEST_USER, TEST_PASSWORD)


@pytest.fixture
def logout_after(main_page: MainPage) -> None:
    """Выходим из под учетки юзера."""
    yield
    if main_page.driver.locator(main_page.profile_button).is_visible():
        main_page.click_logout()


@pytest.fixture
def logout_before(main_page: MainPage) -> None:
    """Выходим из под учетки юзера."""
    if main_page.driver.locator(main_page.profile_button).is_visible():
        main_page.click_logout()
