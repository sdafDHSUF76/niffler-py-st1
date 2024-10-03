from typing import TYPE_CHECKING, Callable

import pytest
from configs import Configs
from tests_ui.pages.profile_page import ProfilePage

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from tests_ui.pages.main_page import MainPage
    from tests_ui.pages.presentation_page import PresentationPage


@pytest.fixture(scope='session')
def profile_page(driver: 'Page') -> ProfilePage:
    """Получаем страницу Profile со всей логикой ее."""
    return ProfilePage(driver)


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
    presentation_page: 'PresentationPage',
    main_page: 'MainPage',
    goto_login_page_and_log_in: Callable[[str, str], None],
) -> None:
    """Перейти на страницу main если не авторизован и находишься на разных местах сайта."""
    if presentation_page.driver.url != ProfilePage.url:
        goto_login_page_and_log_in(Configs.TEST_USER, Configs.TEST_PASSWORD)
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
