from typing import TYPE_CHECKING, Optional

import pytest

from niffler_e_2_e_tests_python.client_api import ClientApi
from niffler_e_2_e_tests_python.configs import FRONT_URL, TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.utils import get_join_url
from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.mark import Mark
    from playwright.sync_api import Page

    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
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
def goto_main_if_you_logged_in(main_page: MainPage) -> None:
    """Перейти на страницу main если авторизован, но находишься на другой странице."""
    if (
        main_page.driver.locator(main_page.main).is_visible()
        and main_page.driver.url != get_join_url(FRONT_URL, MainPage.path)
    ):
        main_page.click(main_page.main)
        # TODO заменить на переход по url


@pytest.fixture
def goto_main_if_you_not_logged_in(
    login_page: 'LoginPage', presentation_page: 'PresentationPage'
) -> None:
    """Перейти на страницу main если не авторизован и находишься на разных местах сайта."""
    if presentation_page.driver.url != get_join_url(FRONT_URL, MainPage.path):
        login_page.goto_login_page_and_log_in(TEST_USER, TEST_PASSWORD)
    # elif presentation_page.driver.url == get_join_url(FRONT_URL, MainPage.path):
    #     # Такой кейс бывает, когда выходишь из учетки и путь в url как раз стоит /main
    #     presentation_page.click_on_login_button()
    #     login_page.authorization(TEST_USER, TEST_PASSWORD)


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
    if main_page.driver.locator(main_page.profile_button).is_visible():
        main_page.click_logout()


@pytest.fixture
def logout_before(main_page: MainPage) -> None:
    """Выходим из под учетки юзера до теста."""
    if main_page.driver.locator(main_page.profile_button).is_visible():
        main_page.click_logout()
