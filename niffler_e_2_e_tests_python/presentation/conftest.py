
from typing import TYPE_CHECKING

import pytest

from niffler_e_2_e_tests_python.configs import FRONT_URL1
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage

if TYPE_CHECKING:
    from playwright.sync_api import Page


@pytest.fixture(scope='session')
def presentation_page(driver: 'Page') -> PresentationPage:
    """Получаем страницу Presentation со всей логикой ее.

    Эта страница, что по этому url Находится http://frontend.niffler.dc
    """
    return PresentationPage(driver)


@pytest.fixture
def goto_presentation_url(presentation_page: PresentationPage) -> None:
    """Перейти на страницу презентации.

    Эта та страница, которая тут http://frontend.niffler.dc
    """
    presentation_page.goto_url(FRONT_URL1)
