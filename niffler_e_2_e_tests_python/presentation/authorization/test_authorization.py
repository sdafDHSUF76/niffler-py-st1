from typing import TYPE_CHECKING

import pytest
from configs import TEST_PASSWORD, TEST_USER
from faker import Faker
from presentation.authorization.enums import ErrorAuthorization
from presentation.authorization.main.conftest import (  # noqa F401
    logout_after,
    logout_before,
    main_page,
)

if TYPE_CHECKING:
    from pages.login_page import LoginPage
    from pages.main_page import MainPage


class TestAuthorization:

    @pytest.mark.usefixtures('go_login_page', 'logout_before', 'logout_after')
    def test_authorization(self, login_page: 'LoginPage', main_page: 'MainPage'):
        login_page.authorization(TEST_USER, TEST_PASSWORD)
        main_page.check_text_of_page_title()

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
    def test_error_hint_for_non_existent_creds(
        self, login: str, password: str, login_page: 'LoginPage',
    ):
        login_page.authorization(login, TEST_PASSWORD)
        login_page.check_hint_text(ErrorAuthorization.INVALID_USER_CREDENTIALS)
