from typing import TYPE_CHECKING

import pytest
from configs import Configs
from tests_ui.pages.main_page import MainPage

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from tests_ui.pages.login_page import LoginPage
    from tests_ui.pages.presentation_page import PresentationPage


pytest_plugins = (
    'tests_ui.presentation.authorization.main.profile.conftest',
    'fixtures.helper_database',
)


@pytest.fixture(scope='session')
def main_page(driver: 'Page') -> MainPage:
    """Получаем страницу Main со всей логикой ее."""
    return MainPage(driver)


@pytest.fixture
def goto_main_if_you_logged_in(main_page: MainPage) -> None:
    """Перейти на страницу main если авторизован, но находишься на другой странице."""
    if (
        main_page.main.is_visible()
        and main_page.driver.url != main_page.url
    ):
        main_page.goto_your_page()


@pytest.fixture
def goto_main_if_you_not_logged_in(
    login_page: 'LoginPage', presentation_page: 'PresentationPage'
) -> None:
    """Перейти на страницу main если не авторизован и находишься на разных местах сайта."""
    if presentation_page.driver.url != MainPage.url:
        login_page.goto_login_page_and_log_in(Configs.TEST_USER, Configs.TEST_PASSWORD)


@pytest.fixture
def goto_main(goto_main_if_you_logged_in: None, goto_main_if_you_not_logged_in: None) -> None:
    """Перейти на страницу main.

    Так как автотест можно запустить один , или запустить целый модуль, то нельзя знать в какой
    момент пользователь будет еще авторизован во время прохождения предыдущих тестов. Чтобы тест
    что будет иметь в себе эту фикстуру не падал из-за разных тестов до него, что были, то решил
    сделать сборную фикстуру, в которой разделил логику перехода на main страницу, когда
    пользователь авторизован и не авторизован.
    """
    pass


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
