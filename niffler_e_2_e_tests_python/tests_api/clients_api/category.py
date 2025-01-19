from typing import TYPE_CHECKING, Union

from configs import Configs
from tests_api.clients_api.authorization import Authorization
from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods
from tests_api.utils.gateway import Gateway

if TYPE_CHECKING:
    from requests import Response
    from tests_api.models.create_category import RequestCreateCategory


class Category(Gateway):
    """API логика, для запросов на категории."""
    def __init__(self, base_url: str | None = None):
        super().__init__(base_url)
        self.token = Authorization().get_token(Configs.TEST_USER, Configs.TEST_PASSWORD)

    def add_category(
        self,
        data_category: Union['RequestCreateCategory', dict],
        user_and_password: tuple[str, str] | None = None,
    ) -> 'Response':
        """Добавить категорию трат."""
        token: str | None = None
        if user_and_password:
            token = Authorization().get_token(Configs.TEST_USER, Configs.TEST_PASSWORD)
        json: dict = (
            data_category if isinstance(data_category, dict) else data_category.model_dump()
        )
        return self.request(
            HttpMethods.POST,
            PathUrl.ADD_CATEGORY,
            json=json,
            headers={'Authorization': token or self.token, 'Content-Type': 'application/json'}
        )
