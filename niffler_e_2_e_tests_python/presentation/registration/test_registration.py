from typing import TYPE_CHECKING

import pytest
from configs import TEST_USER
from faker import Faker
from presentation.authorization.conftest import login_page  # noqa F401
from presentation.authorization.main.conftest import logout_before, main_page  # noqa F401

if TYPE_CHECKING:
    from fixtures.database import DB
    from pages.login_page import LoginPage
    from pages.main_page import MainPage
    from pages.register_page import RegisterPage


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


class TestRegistration:

    @pytest.mark.usefixtures('clear_extra_users', 'logout_before')
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
