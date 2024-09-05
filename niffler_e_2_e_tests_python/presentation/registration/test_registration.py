from typing import TYPE_CHECKING

import allure
import pytest
from faker import Faker

from niffler_e_2_e_tests_python.configs import TEST_USER
from niffler_e_2_e_tests_python.presentation.authorization.conftest import login_page  # noqa F401
from niffler_e_2_e_tests_python.presentation.authorization.main.conftest import (  # noqa F401
    logout_before,
    main_page,
)

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.fixtures.database import DB
    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.registration.register_page import RegisterPage


@pytest.fixture
def clear_extra_users(db_niffler_auth: 'DB'):
    """Чистим созданных юзеров, кроме тестового."""
    yield
    db_niffler_auth.execute(
        'delete from authority'
        ' where user_id in (select id from "user" where username != \'%s\')'
        % TEST_USER,
    )
    db_niffler_auth.execute('delete from "user" where username != \'%s\'' % TEST_USER)


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
        login_page: 'LoginPage',
        main_page: 'MainPage',
    ):
        username: str = Faker().user_name()
        password: str = Faker().password()
        registration_page.register_new_user(username, password)
        login_page.goto_login_page_and_log_in(username, password)
        main_page.check_text_of_page_title()
