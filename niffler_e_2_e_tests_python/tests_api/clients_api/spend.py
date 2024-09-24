from typing import TYPE_CHECKING, Union

from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods
from tests_api.utils.gateway import Gateway

if TYPE_CHECKING:
    from requests import Response
    from tests_api.models.create_spend import RequestCreateSpend


class Spend(Gateway):

    def add_spend(
        self, data_spend: Union['RequestCreateSpend', dict], token: str,
    ) -> 'Response':
        """Добавить трату."""
        json: dict = data_spend if isinstance(data_spend, dict) else data_spend.model_dump()
        return self.request(
            HttpMethods.POST,
            PathUrl.ADD_SPEND,
            json=json,
            headers={'Authorization': token, 'Content-Type': 'application/json'}
        )
