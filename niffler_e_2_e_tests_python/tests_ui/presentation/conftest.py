from typing import TYPE_CHECKING, Callable

import pytest
from configs import Configs
from tests_ui.pages.login_page import LoginPage
from tests_ui.pages.main_page import MainPage
from tests_ui.pages.presentation_page import PresentationPage
from tests_ui.utils.prepare_user import prepare_test_user

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from utils.database import DB

pytest_plugins = ('fixtures.helper_database')


@pytest.fixture(scope='session')
def presentation_page(driver: 'Page') -> PresentationPage:
    """Получаем страницу Presentation со всей логикой ее.

    Эта страница, что по этому url Находится http://frontend.niffler.dc
    """
    return PresentationPage(driver)


@pytest.fixture(scope='session')
def main_page(driver: 'Page') -> MainPage:
    """Получаем страницу Main со всей логикой ее."""
    return MainPage(driver)


@pytest.fixture(scope='session')
def login_page(driver: 'Page') -> LoginPage:
    """Получаем страницу Login со всей логикой ее."""
    return LoginPage(driver)


@pytest.fixture
def logout_before(main_page: MainPage) -> None:
    """Выходим из под учетки юзера до теста."""
    if main_page.profile_button.is_visible():
        main_page.click_logout()
        main_page.check_that_you_not_logged_in()


@pytest.fixture
def goto_presentation_url(presentation_page: PresentationPage) -> None:
    """Перейти на страницу презентации.

    Эта та страница, которая тут http://frontend.niffler.dc/
    """
    if presentation_page.driver.url != presentation_page.url:
        presentation_page.goto_your_page()


@pytest.fixture(scope='session', autouse=True)
def prepare_test_user_for_tests(db_niffler_auth: 'DB'):
    """Создаем тестового юзера.

    Создаем через базу, если юзер есть, то не создаем.
    """
    prepare_test_user(db_niffler_auth)


@pytest.fixture
def goto_login_page_and_log_in(
    presentation_page: PresentationPage, login_page: LoginPage,
) -> Callable[[str, str], None]:
    """Перейти на страницу авторизации и авторизоваться.

    Эти шаги повторяются, поэтому вынес в отдельный метод.
    """
    def _method(username: str, password: str) -> None:
        presentation_page.goto_url(Configs.AUTH_URL)
        presentation_page.click_on_login_button()
        login_page.authorization(username, password)
    return _method
