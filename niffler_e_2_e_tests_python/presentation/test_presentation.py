import pytest

from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    logout_before,
    main_page,
)
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


class TestDisplay:
    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    def test_button_login_is_visible(self, presentation_page: PresentationPage):
        presentation_page.check_visibility_of_login_button()

    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    def test_button_register_is_visible(self, presentation_page: PresentationPage):
        presentation_page.check_visibility_of_register_button()
