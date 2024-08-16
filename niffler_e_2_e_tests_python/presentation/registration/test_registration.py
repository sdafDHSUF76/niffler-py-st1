from typing import TYPE_CHECKING, Callable

import pytest
from faker import Faker
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.presentation.authorization.conftest import login_page  # noqa F401
from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    main_page,
)

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.registration.register_page import RegisterPage


class TestRegistration:

    @pytest.mark.usefixtures('clear_extra_users', 'logout')
    def test_authorization_with_create_user_random(
        self,
        registration_page: 'RegisterPage',
        go_login_page_function: Callable[[], None],
        login_page: 'LoginPage',
        main_page: 'MainPage',
    ):
        username: str = Faker().user_name()
        password: str = Faker().password()
        registration_page.register_new_user(username, password)
        go_login_page_function()
        login_page.authorization(username, password)
        expect(main_page.driver.locator(main_page.header)).to_have_text(main_page.text_header)
