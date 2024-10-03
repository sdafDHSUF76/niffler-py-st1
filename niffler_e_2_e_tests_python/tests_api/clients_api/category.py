from typing import TYPE_CHECKING, Union

from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods
from tests_api.utils.gateway import Gateway

if TYPE_CHECKING:
    from requests import Response
    from tests_api.models.create_category import RequestCreateCategory


class Category(Gateway):
    """API логика, для запросов на категории."""
    def add_category(
        self, data_category: Union['RequestCreateCategory', dict], token: str
    ) -> 'Response':
        """Добавить категорию трат."""
        json: dict = (
            data_category if isinstance(data_category, dict) else data_category.model_dump()
        )
        return self.request(
            HttpMethods.POST,
            PathUrl.ADD_CATEGORY,
            json=json,
            headers={'Authorization': token, 'Content-Type': 'application/json'}
        )
