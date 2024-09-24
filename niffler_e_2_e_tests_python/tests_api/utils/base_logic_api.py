from typing import TYPE_CHECKING, Union

from requests import Session
from tests_api.utils.allure_helper import allure_attach_request

if TYPE_CHECKING:
    from requests import Response
    from tests_api.clients_api.constants.api_paths import PathUrl
    from tests_api.enums.http_methods import HttpMethods


class BaseLogicApi(Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    @allure_attach_request
    def request(
        self, method: 'HttpMethods',
        url: Union[str, 'PathUrl'],
        **other_fields_for_request_request
    ) -> 'Response':
        """Логирование запроса и вклейка base_url."""
        return super().request(method.name, self.base_url + url, **other_fields_for_request_request)
