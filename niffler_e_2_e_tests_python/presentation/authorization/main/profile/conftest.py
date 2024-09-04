from typing import TYPE_CHECKING, Optional

import pytest

from niffler_e_2_e_tests_python.client_api import ClientApi
from niffler_e_2_e_tests_python.configs import FRONT_URL, TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.fixtures.database import db_niffler_spend  # noqa F401
from niffler_e_2_e_tests_python.presentation.authorization.main.profile.profile_page import (
    ProfilePage,
)
from niffler_e_2_e_tests_python.utils import get_join_url

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.mark import Mark
    from playwright.sync_api import Page

    from niffler_e_2_e_tests_python.fixtures.database import DB
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.fixture(scope='session')
def profile_page(driver: 'Page') -> ProfilePage:
    """Получаем страницу Profile со всей логикой ее."""
    return ProfilePage(driver)


@pytest.fixture
def clear_spend_and_category_after(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category и spend."""
    yield
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    db_niffler_spend.execute('delete from category')


@pytest.fixture(scope='class')
def clear_spend_and_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category и spend."""
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def goto_profile_if_you_logged_in(profile_page: ProfilePage) -> None:
    """Перейти на страницу main если авторизован, но находишься на другой странице."""
    if (
        profile_page.profile_button.is_visible()
        and profile_page.driver.url != profile_page.url
    ):
        profile_page.goto_your_page()


@pytest.fixture
def goto_profile_if_you_not_logged_in(
    login_page: 'LoginPage', presentation_page: 'PresentationPage', main_page: 'MainPage'
) -> None:
    """Перейти на страницу main если не авторизован и находишься на разных местах сайта."""
    if presentation_page.driver.url != ProfilePage.url:
        login_page.goto_login_page_and_log_in(TEST_USER, TEST_PASSWORD)
        main_page.click_profile_button()


@pytest.fixture
def goto_profile(
    goto_profile_if_you_logged_in: None, goto_profile_if_you_not_logged_in: None,
):
    """Перейти на страницу profile из разных мест сайта.

    Так как автотест можно запустить один , или запустить целый модуль, то нельзя знать в какой
    момент пользователь будет еще авторизован во время прохождения предыдущих тестов. Чтобы тест
    что будет иметь в себе эту фикстуру не падал из-за разных тестов до него, что были, то решил
    сделать сборную фикстуру, в которой разделил логику перехода на main страницу, когда
    пользователь авторизован и не авторизован.
    """
    pass


@pytest.fixture
def create_categories(request: 'SubRequest'):
    """Создаем категории через API.

    На самом деле тут только через API категория создается, а вот токен берется из UI.
    """
    marker: Optional['Mark'] = request.node.get_closest_marker('parameter_data')
    user_old, password_old = None, None
    for unit in marker.args:
        user, password = unit['user'], unit['password']
        if user_old != user and password_old != password:
            token: str = ClientApi().get_token(unit['user'], unit['password'])
        ClientApi().add_category(unit['category'], token)
        user_old, password_old = user, password
