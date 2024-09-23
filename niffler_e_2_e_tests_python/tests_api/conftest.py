from typing import TYPE_CHECKING

import pytest

from configs import configs
from tests_api.clients_api.client_api import AuthorizationApi
from fixtures.helper_database import clear_category
if TYPE_CHECKING:
    from utils.database import DB


pytest_plugins = ('fixtures.helper_database')


# @pytest.fixture
# def get_token() -> str:
#     return AuthorizationApi().get_token(configs['TEST_USER'], configs['TEST_PASSWORD'])
