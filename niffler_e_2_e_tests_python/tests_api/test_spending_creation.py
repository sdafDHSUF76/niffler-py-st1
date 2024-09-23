from datetime import datetime, timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

from configs import configs
from tests_api.clients_api.client_api import AuthorizationApi
from tests_api.clients_api.hidden_client_api import HiddenClientApi
from tests_api.enums.currencies import Currencies
from tests_api.enums.spend_errors import Type, Title, Detail
from tests_api.models.create_category import RequestCreateCategory
from tests_api.models.create_spend import RequestCreateSpend, ResponseCreateSpend, \
    ResponseErrorCreateSpend

if TYPE_CHECKING:
    from requests import Response


@pytest.mark.usefixtures('clear_spend_and_category')
class TestSuccess:
    def test_create_category(self):
        spend = {
            "amount": "45",
            "description": "ee",
            "category": "fgh",
            "spendDate": "2024-09-22T14:13:49.814Z",
            "currency": Currencies.RUB,
        }
        token: str = AuthorizationApi().get_token(configs['TEST_USER'], configs['TEST_PASSWORD'])

        HiddenClientApi().add_category(RequestCreateCategory(category=spend['category']), token)

        response: 'Response' = HiddenClientApi().add_spend(RequestCreateSpend(**spend), token)

        assert response.status_code == HTTPStatus.CREATED
        response: ResponseCreateSpend = ResponseCreateSpend.model_validate(response.json())
        assert response.username == configs['TEST_USER']
        assert response.description == 'ee'
        assert response.currency == Currencies.RUB.name
        assert response.category == 'fgh'
        assert (
            datetime.fromisoformat(spend['spendDate'].replace('Z', ''))
            == datetime.fromisoformat(response.spendDate).replace(tzinfo=None)
        ), (
            'время из запроса не совпало со временем из response\n'
            f'Ожидаем: {datetime.fromisoformat(spend["spendDate"].replace("Z", ""))}\n'
            f'Получаем: {datetime.fromisoformat(response.spendDate).replace(tzinfo=None)}'
        )
        assert timedelta(0) == datetime.fromisoformat(response.spendDate).utcoffset(), (
            'таймзона не Utc в response'
        )

@pytest.mark.usefixtures('clear_spend_and_category')
class TestNegative:
    def test_invalid_date_format(self):
        spend = {
            "amount": "45",
            "description": "ee",
            "category": "fgh",
            "spendDate": "2024-09-22 14:13:49.814Z",
            "currency": Currencies.RUB.name,
        }
        token: str = AuthorizationApi().get_token(configs['TEST_USER'], configs['TEST_PASSWORD'])

        HiddenClientApi().add_category(RequestCreateCategory(category=spend['category']), token)
        response: 'Response' = HiddenClientApi().add_spend(spend, token)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        response: ResponseErrorCreateSpend = ResponseErrorCreateSpend.model_validate(response.json())
        assert response.type == Type.default.value
        assert response.title == Title.bad_request.value
        assert response.status == HTTPStatus.BAD_REQUEST
        assert response.instance == '/api/spends/add'
        assert response.detail == Detail.bad_request.value
