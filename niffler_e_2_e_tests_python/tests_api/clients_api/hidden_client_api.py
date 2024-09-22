from configs import configs
from tests_api.clients_api.base_api import BaseApi
from tests_api.clients_api.enums import HttpMethods


class HiddenClientApi(BaseApi):
    def __init__(self, base_url: str = configs['GATEWAY_URL']):
        super().__init__(base_url)

    def add_spend(self, data_spend: dict, token: str) -> None:
        """Добавить трату."""
        self.request(
            HttpMethods.POST,
            '/api/spends/add',
            json=data_spend,
            headers={'Authorization': token, 'Content-Type': 'application/json'}
        )

    def add_category(self, data_category: dict, token: str) -> None:
        """Добавить категорию трат."""
        self.request(
            HttpMethods.POST,
            '/api/categories/add',
            json=data_category,
            headers={'Authorization': token, 'Content-Type': 'application/json'}
        )