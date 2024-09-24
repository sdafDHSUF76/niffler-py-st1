from http import HTTPStatus
from typing import TYPE_CHECKING

from configs import Configs
from tests_api.clients_api.client_api import AuthorizationApi

if TYPE_CHECKING:

    from requests import Response
    from utils.database import DB


def prepare_test_user(db_niffler_auth: 'DB') -> None:
    """Создаем тестового юзера.

    Создаем через базу, если юзер есть, то не создаем.
    """
    number_of_users: int = db_niffler_auth.get_value(
        'select count(*) from "user" where username = \'%s\'' % Configs.TEST_USER,
    )[0][0]
    if not number_of_users:
        response: 'Response' = AuthorizationApi().create_user(
            Configs.TEST_USER, Configs.TEST_PASSWORD,
        )
        assert response.status_code == HTTPStatus.CREATED
        assert len(response.history) == 0
