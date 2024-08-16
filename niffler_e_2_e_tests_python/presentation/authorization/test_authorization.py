from typing import TYPE_CHECKING

import pytest
from faker import Faker
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.presentation.authorization.enums import ErrorAuthorization
from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    main_page,
)

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage


@pytest.mark.usefixtures('prepare_test_user')
class TestAuthorization:

    @pytest.mark.usefixtures('go_login_page', 'logout', 'clear_storage')
    def test_authorization(self, login_page: 'LoginPage', main_page: 'MainPage'):
        login_page.authorization(TEST_USER, TEST_PASSWORD)
        expect(main_page.driver.locator(main_page.header)).to_have_text(main_page.text_header)

    @pytest.mark.usefixtures('go_login_page')
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
    def test_error_text_for_non_existent_creds(
        self, login: str, password: str, login_page: 'LoginPage'
    ):
        login_page.authorization(login, TEST_PASSWORD)
        expect(login_page.driver.locator(login_page.text_error)).to_have_text(
            ErrorAuthorization.INVALID_USER_CREDENTIALS,
        )
