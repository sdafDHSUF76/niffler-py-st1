from typing import TYPE_CHECKING

import pytest
from tests_ui.pages.register_page import RegisterPage

if TYPE_CHECKING:
    from playwright.sync_api import Page


@pytest.fixture(scope='session')
def registration_page(driver: 'Page') -> RegisterPage:
    """Получаем страницу Register со всей логикой ее."""
    return RegisterPage(driver)


@pytest.fixture
def goto_registration_url(registration_page: RegisterPage) -> None:
    """Переходим на страницу Register."""

    if registration_page.driver.url != registration_page.url:
        registration_page.goto_your_page()
