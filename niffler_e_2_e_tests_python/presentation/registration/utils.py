from http import HTTPStatus
from typing import TYPE_CHECKING

from niffler_e_2_e_tests_python.client_api import ClientApi
from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER

if TYPE_CHECKING:

    from requests import Response

    from niffler_e_2_e_tests_python.fixtures.database import DB


def prepare_test_user(db_niffler_auth: 'DB') -> None:
    """Создаем тестового юзера.

    Создаем через базу, если юзер есть, то не создаем.
    """
    number_of_users: int = db_niffler_auth.get_value(
        'select count(*) from "user" where username = \'%s\'' % TEST_USER,
    )[0][0]
    if not number_of_users:
        response: 'Response' = ClientApi().create_user(TEST_USER, TEST_PASSWORD)
        assert response.status_code == HTTPStatus.CREATED
        assert len(response.history) == 0
