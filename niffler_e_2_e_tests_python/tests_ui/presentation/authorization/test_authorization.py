from typing import TYPE_CHECKING

import allure
import pytest
from configs import Configs
from faker import Faker
from tests_ui.presentation.authorization.enums import ErrorAuthorization

if TYPE_CHECKING:
    from pages.login_page import LoginPage
    from pages.main_page import MainPage


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
    @allure.step
    def test_authorization(self, login_page: 'LoginPage', main_page: 'MainPage'):
        login_page.authorization(Configs.TEST_USER, Configs.TEST_PASSWORD)
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
    @allure.story(
        'user authentication',
        'display field hints in case of authentication error',
        'create a database to store registered users',
        'create hints on the form, if the data sent is invalid',
    )
    @allure.step
    def test_error_hint_for_non_existent_creds(
        self, login: str, password: str, login_page: 'LoginPage',
    ):
        login_page.authorization(login, Configs.TEST_PASSWORD)
        login_page.check_hint_text(ErrorAuthorization.INVALID_USER_CREDENTIALS)
