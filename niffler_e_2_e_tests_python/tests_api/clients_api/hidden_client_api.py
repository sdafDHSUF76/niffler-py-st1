from typing import TYPE_CHECKING

from configs import Configs
from tests_api.clients_api.base_api import BaseApi
from tests_api.enums.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods
from tests_api.models.create_category import RequestCreateCategory
from tests_api.models.create_spend import RequestCreateSpend

if TYPE_CHECKING:
    from requests import Response


class HiddenClientApi(BaseApi):
    def __init__(self, base_url: str = Configs.GATEWAY_URL):
        super().__init__(base_url)

    def add_spend(self, data_spend: RequestCreateSpend | dict, token: str) -> 'Response':
        """Добавить трату."""
        json: dict = data_spend if isinstance(data_spend, dict) else data_spend.model_dump()
        return self.request(
            HttpMethods.POST,
            PathUrl.add_spend.value,
            json=json,
            headers={'Authorization': token, 'Content-Type': 'application/json'}
        )

    def add_category(self, data_category: RequestCreateCategory | dict, token: str) -> 'Response':
        """Добавить категорию трат."""
        json: dict = (
            data_category if isinstance(data_category, dict) else data_category.model_dump()
        )
        return self.request(
            HttpMethods.POST,
            PathUrl.add_category.value,
            json=json,
            headers={'Authorization': token, 'Content-Type': 'application/json'}
        )
