import allure
import pytest

from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    logout_before,
    main_page,
)
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@allure.epic(
    'Presentation page',
    'features (what the user can do) for an unauthorized\\authorized user',
)
@allure.feature(
    'features (what the user can do) for an unauthorized user',
    'Creating a presentation form',
)
class TestDisplay:
    @allure.story(
        'displaying the authorization and registration buttons',
    )
    @pytest.mark.parametrize(
        "button_locator",
        [PresentationPage.button_login, PresentationPage.button_register],
        ids=[i for i in [PresentationPage.button_login, PresentationPage.button_register]]
    )
    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    def test_buttons_visible(self, button_locator: str, presentation_page: PresentationPage):
        presentation_page.check_element_is_visible(button_locator)
