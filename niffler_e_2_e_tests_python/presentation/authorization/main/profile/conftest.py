from typing import TYPE_CHECKING, Callable, Optional

import pytest
import requests

from niffler_e_2_e_tests_python.configs import FRONT_URL1, GATEWAY_URL, TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.fixtures.database import db_niffler_spend  # noqa F401
from niffler_e_2_e_tests_python.presentation.authorization.main.profile.profile_page import (
    ProfilePage,
)

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest
    from _pytest.mark import Mark
    from playwright.sync_api import Page

    from niffler_e_2_e_tests_python.fixtures.database import DB
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.fixture(scope='class')
def profile_page(driver: 'Page') -> ProfilePage:
    """Получаем страницу Profile со всей логикой ее."""
    return ProfilePage(driver)


@pytest.fixture
def clear_category(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    yield
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_spend(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу spend."""
    yield
    db_niffler_spend.execute('delete from spend')


@pytest.fixture(scope='class')
def clear_spend_and_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category и spend."""
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_spend_and_category_after(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category и spend."""
    yield
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def goto_profile(
    login_page: 'LoginPage', main_page: 'MainPage', presentation_page: 'PresentationPage',
):
    if (
        main_page.driver.locator(main_page.profile).is_visible()
        and main_page.driver.url != f'{FRONT_URL1}{ProfilePage.path}'
    ):
        main_page.click(main_page.profile)
    if presentation_page.driver.url != f'{FRONT_URL1}{ProfilePage.path}':
        presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)
        login_page.authorization(TEST_USER, TEST_PASSWORD)
        main_page.click(main_page.profile)


@pytest.fixture
def reload_profile_page(db_niffler_spend: 'DB', profile_page: ProfilePage):
    category_in_db = db_niffler_spend.get_value(
        'select count(*) from category where username = \'%s\'' % TEST_USER
    )[0][0]
    category_in_front = profile_page.driver.locator(profile_page.categories_list).count()
    if (
        profile_page.driver.url == f'{FRONT_URL1}{ProfilePage.path}'
        and category_in_db != category_in_front
    ):
        profile_page.driver.reload()


@pytest.fixture
def close_alert(profile_page: 'ProfilePage'):
    yield
    profile_page.click(profile_page.alert_button_close)


@pytest.fixture
def create_categories(get_token: Callable[[str, str], str], request: 'SubRequest'):
    """Создаем категории через API.

    На самом деле тут только через API категория создается, а вот токен берется из UI.
    """
    marker: Optional['Mark'] = request.node.get_closest_marker('parameter_data')
    user_old, password_old = None, None
    for unit in marker.args:
        user, password = unit['user'], unit['password']
        if user_old != user and password_old != password:
            token: str = get_token(unit['user'], unit['password'])
        requests.post(
            f'{GATEWAY_URL}/api/categories/add',
            json=unit['category'],
            headers={
                'Authorization': token,
                'Content-Type': 'application/json',
            }
        )
        user_old, password_old = user, password
