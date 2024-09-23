from typing import TYPE_CHECKING

import pytest
from configs import configs
from pages.profile_page import ProfilePage

if TYPE_CHECKING:
    from pages.login_page import LoginPage
    from pages.main_page import MainPage
    from pages.presentation_page import PresentationPage
    from playwright.sync_api import Page
    from utils.database import DB


pytest_plugins = ('fixtures.helper_database', 'fixtures.helper_category')


@pytest.fixture(scope='session')
def profile_page(driver: 'Page') -> ProfilePage:
    """Получаем страницу Profile со всей логикой ее."""
    return ProfilePage(driver)


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
        login_page.goto_login_page_and_log_in(configs['TEST_USER'], configs['TEST_PASSWORD'])
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
