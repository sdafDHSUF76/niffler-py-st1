import pytest
from pages.presentation_page import PresentationPage
from tests.authorization.main.conftest import logout_before, main_page  # noqa F401


class TestDisplay:
    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    def test_button_login_is_visible(self, presentation_page: PresentationPage):
        presentation_page.check_visibility_of_login_button()

    @pytest.mark.usefixtures('logout_before', 'goto_presentation_url')
    def test_button_register_is_visible(self, presentation_page: PresentationPage):
        presentation_page.check_visibility_of_register_button()
