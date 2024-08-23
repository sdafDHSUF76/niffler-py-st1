from typing import TYPE_CHECKING, Callable

import pytest
from faker import Faker

from niffler_e_2_e_tests_python.presentation.authorization.conftest import (  # noqa F401
    go_login_page_function,
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


class TestRegistration:

    @pytest.mark.usefixtures('clear_extra_users', 'logout_before')
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
        main_page.check_text_in_element(main_page.header, main_page.text_header)
