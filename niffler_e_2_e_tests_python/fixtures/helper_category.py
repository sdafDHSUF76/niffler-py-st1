from typing import Optional

import pytest
from _pytest.fixtures import SubRequest
from _pytest.mark import Mark
from tests_api.clients_api.authorization import Authorization
from tests_api.clients_api.category import Category
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
            user_and_password: tuple[str, str] = (unit['user'], unit['password'])
        Category().add_category(
            RequestCreateCategory(**unit['category']), user_and_password,
        )
        user_old, password_old = user, password
