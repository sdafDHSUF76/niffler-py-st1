import requests
from requests import Session

from tests_api.clients_api.enums import HttpMethods
from tests_api.utils.allure_helper import allure_attach_request


class BaseApi(Session):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    @allure_attach_request
    def request(self, method: 'HttpMethods', url: str, **other_fields_for_request_request):
        """Логирование запроса и вклейка base_url."""
        return super().request(method.name, self.base_url + url, **other_fields_for_request_request)
