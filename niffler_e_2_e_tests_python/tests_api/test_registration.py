from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from tests_api.clients_api.user import User

if TYPE_CHECKING:
    from requests import Response
    from utils.database import DB


@pytest.mark.usefixtures('clear_extra_users')
class TestSuccess:

    def test_registration(self):
        response: 'Response' = User().create_user('vbn', 'hjk')
        assert response.status_code == HTTPStatus.CREATED
        assert response.text
        # TODO сделать парсер, что пришла html и все, что тут конкретно еще проверить не скажу

    def test_check_database_after_user_registration(self, db_niffler_auth: 'DB'):
        """Проверяется тут не только, что юзер в базе данных верный создался.

        Тут также проверяются определенные права у юзера при создании.
        """
        username = 'vbn'
        User().create_user(username, 'hjk')
        result_query: None | str = db_niffler_auth.get_value(
            'select 1 from "user"'
            ' where username = \'%s\''
            ' and enabled is true'
            ' and account_non_expired is true'
            ' and account_non_locked is true'
            ' and credentials_non_expired is true'
            % username
        )[0][0]
        assert result_query, (
            f'Не нашелся такой юзер: {username}, по query выше\n'
            'Проверьте вручную в базе данных, что там.'
        )
