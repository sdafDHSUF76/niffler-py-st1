import pytest
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.configs import FRONT_URL1
from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    logout_before,
    main_page,
)
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.fixture(scope='class')
def goto_main_url(presentation_page: PresentationPage) -> None:
    presentation_page.goto_url(FRONT_URL1)


@pytest.mark.parametrize(
    "button_locator",
    [PresentationPage.button_login, PresentationPage.button_register],
    ids=[i for i in [PresentationPage.button_login, PresentationPage.button_register]]
)
@pytest.mark.usefixtures('logout_before', 'goto_main_url')
def test_buttons_visible(button_locator: str, presentation_page: PresentationPage):
    expect(presentation_page.driver.locator(button_locator)).to_be_visible()
