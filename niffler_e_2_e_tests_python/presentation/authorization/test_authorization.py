from typing import TYPE_CHECKING

import allure
import pytest
from faker import Faker

from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.presentation.authorization.enums import ErrorAuthorization
from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    logout_after,
    logout_before,
    main_page,
)

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage


@allure.epic(
    'Authorization page',
    'features (what the user can do) for an unauthorized\\authorized user',
)
@allure.feature(
    'features (what the user can do) for an unauthorized user',
    'User authorization',
)
class TestAuthorization:

    @allure.story(
        'user authentication',
        'After successful authorization, show the main page',
        'Upon successful authorization, show the main page',
        'create a database to store registered users',
    )
    @pytest.mark.usefixtures('go_login_page', 'logout_before', 'logout_after')
    def test_authorization(self, login_page: 'LoginPage', main_page: 'MainPage'):
        login_page.authorization(TEST_USER, TEST_PASSWORD)
        main_page.check_text_in_element(main_page.header, main_page.text_header)

    @pytest.mark.usefixtures('go_login_page', 'logout_before')
    @pytest.mark.parametrize(
        'login, password',
        [
            ('asdf', 'asdf'),
            ('qwer', 'qwer'),
            ('we', 'we'),
            (' ', ' '),
            ('  ', '  '),
            ('\32%$^&*(', '\32%$^&*('),
            (Faker().user_name(), Faker().password()),
        ]
    )
    @allure.story(
        'user authentication',
        'display field hints in case of authentication error',
        'create a database to store registered users',
        'create hints on the form, if the data sent is invalid',
    )
    def test_error_text_for_non_existent_creds(
        self, login: str, password: str, login_page: 'LoginPage'
    ):
        login_page.authorization(login, TEST_PASSWORD)
        login_page.check_text_in_element(
            login_page.text_error, ErrorAuthorization.INVALID_USER_CREDENTIALS,
        )
