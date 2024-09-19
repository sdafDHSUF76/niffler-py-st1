from http import HTTPStatus
from typing import TYPE_CHECKING

from configs import configs
from utils.client_api import ClientApi

if TYPE_CHECKING:

    from utils.database import DB
    from requests import Response


def prepare_test_user(db_niffler_auth: 'DB') -> None:
    """Создаем тестового юзера.

    Создаем через базу, если юзер есть, то не создаем.
    """
    number_of_users: int = db_niffler_auth.get_value(
        'select count(*) from "user" where username = \'%s\'' % configs['TEST_USER'],
    )[0][0]
    if not number_of_users:
        response: 'Response' = ClientApi().create_user(
            configs['TEST_USER'], configs['TEST_PASSWORD'],
        )
        assert response.status_code == HTTPStatus.CREATED
        assert len(response.history) == 0
