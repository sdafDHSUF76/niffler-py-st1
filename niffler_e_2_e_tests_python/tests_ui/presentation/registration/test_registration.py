from typing import TYPE_CHECKING, Callable

import allure
import pytest
from faker import Faker

if TYPE_CHECKING:
    from tests_ui.pages.main_page import MainPage
    from tests_ui.pages.register_page import RegisterPage


@allure.story('User registration via the UI')
class TestRegistration:

    @allure.feature(
        'Create a user through the ui',
        'create a database to store registered users',
        'Upon successful authorization, show the main page',
        'user authentication',
    )
    @pytest.mark.usefixtures('clear_extra_users', 'logout_before')
    @allure.step
    def test_authorization_with_create_user_random(
        self,
        registration_page: 'RegisterPage',
        main_page: 'MainPage',
        goto_login_page_and_log_in: Callable[[str, str], None],
    ):
        username: str = Faker().user_name()
        password: str = Faker().password()
        registration_page.register_user(username, password)
        goto_login_page_and_log_in(username, password)
        main_page.check_text_of_page_title()
