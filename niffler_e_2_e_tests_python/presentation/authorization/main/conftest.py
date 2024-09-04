from typing import TYPE_CHECKING

import pytest

from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.fixture(scope='session')
def main_page(driver: 'Page') -> MainPage:
    """Получаем страницу Main со всей логикой ее."""
    return MainPage(driver)


@pytest.fixture
def logout_after(main_page: MainPage) -> None:
    """Выходим из под учетки юзера после теста."""
    yield
    if main_page.profile_button.is_visible():
        main_page.click_logout()
        main_page.check_that_you_not_logged_in()


@pytest.fixture
def logout_before(main_page: MainPage) -> None:
    """Выходим из под учетки юзера до теста."""
    if main_page.profile_button.is_visible():
        main_page.click_logout()
        main_page.check_that_you_not_logged_in()
