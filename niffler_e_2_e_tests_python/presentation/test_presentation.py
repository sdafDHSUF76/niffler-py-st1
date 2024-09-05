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
    @allure.story('displaying buttons on the presentation page')
    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    @allure.step
    def test_button_login_is_visible(self, presentation_page: PresentationPage):
        presentation_page.check_visibility_of_login_button()

    @allure.story('displaying buttons on the presentation page')
    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    @allure.step
    def test_button_register_is_visible(self, presentation_page: PresentationPage):
        presentation_page.check_visibility_of_register_button()
