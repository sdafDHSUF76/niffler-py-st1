from typing import TYPE_CHECKING

import pytest

from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage

if TYPE_CHECKING:
    from playwright.sync_api import Page


@pytest.fixture(scope='class')
def main_page(driver: 'Page') -> MainPage:
    """Получаем страницу Main со всей логикой ее."""
    return MainPage(driver)
