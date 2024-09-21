from typing import TYPE_CHECKING

import allure
import pytest
from configs import configs
from faker import Faker

if TYPE_CHECKING:
    from pages.login_page import LoginPage
    from pages.main_page import MainPage
    from pages.register_page import RegisterPage
    from utils.database import DB


@pytest.fixture
def clear_extra_users(db_niffler_auth: 'DB'):
    """Чистим созданных юзеров, кроме тестового."""
    yield
    db_niffler_auth.execute(
        'delete from authority'
        ' where user_id in (select id from "user" where username != \'%s\')'
        % configs['TEST_USER'],
    )
    db_niffler_auth.execute('delete from "user" where username != \'%s\'' % configs['TEST_USER'])


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
        registration_page.register_user(username, password)
        login_page.goto_login_page_and_log_in(username, password)
        main_page.check_text_of_page_title()
