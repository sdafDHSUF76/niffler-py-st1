from typing import TYPE_CHECKING

import allure
import pytest
from faker import Faker

from niffler_e_2_e_tests_python.presentation.authorization.conftest import (  # noqa F401
    login_page,
)
from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    logout_before,
    main_page,
)

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.registration.register_page import RegisterPage


@allure.story('User registration via the UI')
class TestRegistration:

    @allure.feature(
        'Create a user through the ui',
        'create a database to store registered users',
        'Upon successful authorization, show the main page',
        'user authentication',
    )
    @pytest.mark.usefixtures('clear_extra_users', 'logout_before')
    def test_authorization_with_create_user_random(
        self,
        registration_page: 'RegisterPage',
        login_page: 'LoginPage',
        main_page: 'MainPage',
    ):
        username: str = Faker().user_name()
        password: str = Faker().password()
        registration_page.register_new_user(username, password)
        login_page.goto_login_page()
        login_page.authorization(username, password)
        main_page.check_text_in_element(main_page.header, main_page.text_header)
