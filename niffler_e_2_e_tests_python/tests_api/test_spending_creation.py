from datetime import datetime, timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from configs import Configs
from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.clients_api.constants.spend_errors import Detail, Title, Type
from tests_api.clients_api.spend import Spend
from tests_api.enums.currencies import Currencies
from tests_api.models.create_spend import (
    RequestCreateSpend,
    ResponseCreateSpend,
    ResponseErrorCreateSpend,
)

if TYPE_CHECKING:
    from requests import Response


class TestSuccess:

    @pytest.mark.parameter_data(
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'fgh'},
        },
    )
    @pytest.mark.usefixtures('clear_spend_and_category', 'create_categories')
    def test_create_spend(self):
        spend = {
            "amount": "45",
            "description": "ee",
            "category": "fgh",
            "spendDate": "2024-09-22T14:13:49.814Z",
            "currency": Currencies.RUB.name,
        }
        response: 'Response' = Spend().add_spend(RequestCreateSpend(**spend))

        assert response.status_code == HTTPStatus.CREATED
        response: ResponseCreateSpend = ResponseCreateSpend.model_validate(response.json())
        assert response.username == Configs.TEST_USER
        assert response.description == spend['description']
        assert response.currency == Currencies.RUB.name
        assert response.category == spend['category']
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


class TestNegative:

    @pytest.mark.parameter_data(
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'fgh'},
        },
    )
    @pytest.mark.usefixtures('clear_spend_and_category', 'create_categories')
    def test_invalid_date_format_date_in_request_body(self):
        spend = {
            "amount": "45",
            "description": "ee",
            "category": "fgh",
            "spendDate": "2024-09-22 14:13:49.814Z",
            "currency": Currencies.RUB.name,
        }
        expected_response: ResponseErrorCreateSpend = (
            ResponseErrorCreateSpend(
                type=Type.DEFAULT,
                title=Title.BAD_REQUEST,
                status=HTTPStatus.BAD_REQUEST,
                instance=PathUrl.ADD_SPEND,
                detail=Detail.BAD_REQUEST,
            )
        )

        response: 'Response' = Spend().add_spend(spend)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        current_response: ResponseErrorCreateSpend = (
            ResponseErrorCreateSpend.model_validate(response.json())
        )
        assert current_response == expected_response
