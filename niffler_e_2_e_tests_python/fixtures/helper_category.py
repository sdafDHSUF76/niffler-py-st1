from typing import Optional

import pytest
from _pytest.fixtures import SubRequest
from _pytest.mark import Mark
from tests_api.clients_api.client_api import AuthorizationApi
from tests_api.clients_api.hidden_client_api import HiddenClientApi
from tests_api.models.create_category import RequestCreateCategory


@pytest.fixture
def create_categories(request: 'SubRequest'):
    """Создаем категории через API.

    На самом деле тут только через API категория создается, а вот токен берется из UI.
    """
    marker: Optional['Mark'] = request.node.get_closest_marker('parameter_data')
    user_old, password_old = None, None
    for unit in marker.args:
        user, password = unit['user'], unit['password']
        if user_old != user and password_old != password:
            token: str = AuthorizationApi().get_token(unit['user'], unit['password'])
        HiddenClientApi().add_category(
            RequestCreateCategory(**unit['category']), token,
        )
        user_old, password_old = user, password
