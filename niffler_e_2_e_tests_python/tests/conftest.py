from typing import TYPE_CHECKING

import pytest
from pages.presentation_page import PresentationPage
from tests.registration.utils.utils import prepare_test_user

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from utils.database import DB

pytest_plugins = ('tests.authorization.main.conftest')


@pytest.fixture(scope='session')
def presentation_page(driver: 'Page') -> PresentationPage:
    """Получаем страницу Presentation со всей логикой ее.

    Эта страница, что по этому url Находится http://frontend.niffler.dc
    """
    return PresentationPage(driver)


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
