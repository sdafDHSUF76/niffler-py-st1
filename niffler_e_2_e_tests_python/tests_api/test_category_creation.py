from datetime import datetime
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
import pytz as pytz
from configs import Configs
from tests_api.clients_api.category import Category
from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.clients_api.constants.category_errors import Error
from tests_api.models.create_category import (
    RequestCreateCategory,
    ResponseCreateCategory,
    ResponseErrorCreateCategory,
)

if TYPE_CHECKING:
    from requests import Response
    from utils.database import DB


@pytest.mark.usefixtures('clear_category')
class TestSuccess:
    def test_create_category(self):
        category = 'sdf'

        response: 'Response' = Category().add_category(
            RequestCreateCategory(category=category),
        )

        assert response.status_code == HTTPStatus.OK
        response: ResponseCreateCategory = ResponseCreateCategory.model_validate(response.json())
        assert response.username == Configs.TEST_USER
        assert response.category == category

    def test_check_created_category_in_database(self, db_niffler_spend: 'DB'):
        category = 'sdf'

        response: 'Response' = Category().add_category(
            RequestCreateCategory(category=category),
        )

        db_category, db_username = db_niffler_spend.get_value(
            'select category, username from category where id = \'%s\''
            % response.json()['id']
        )[0]
        assert db_category == category
        assert db_username == Configs.TEST_USER


@pytest.mark.usefixtures('clear_category')
class TestUniqueCategory:

    def test_create_non_unique_category(self):
        category = 'sdf'
        moscow_timezone: pytz.UTC = pytz.timezone('Europe/Moscow')
        now: datetime = datetime.now(moscow_timezone).replace(tzinfo=None)

        Category().add_category(
            RequestCreateCategory(category=category),
        )
        response: 'Response' = Category().add_category(
            RequestCreateCategory(category=category),
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        response: ResponseErrorCreateCategory = ResponseErrorCreateCategory.model_validate(
            response.json(),
        )
        assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.path == PathUrl.ADD_CATEGORY
        assert response.error == Error.INTERNAL_SERVER_ERROR
        timestamp: datetime = (
            datetime.fromisoformat(response.timestamp).astimezone(moscow_timezone).replace(
                tzinfo=None,
            )
        )
        assert 0 < (timestamp - now).total_seconds() < 2, (
            'Время создания категории произошла вне рамок 2 секунд:\n'
            f'время в response: {timestamp}'
            f'время в отсчета: {now}'
            'Разница между ними (timestamp - now).total_seconds() = '
            f'{(timestamp - now).total_seconds()}'
        )


@pytest.mark.usefixtures('clear_category')
class TestCategoryTitle:

    @pytest.mark.parametrize(
        'category',
        ('^M,asdf \n, asdf\r', '♣ ☺', "[|]'~<!--@/*$%^&#*/()?>,.*/\\", 'àáâãäåçèéêëìíîðñòôõöö'),
        ids=('End of line', 'emojis', 'special characters', 'Symbols with stress marks')
    )
    def test_different_names_category(self, category: str, db_niffler_spend: 'DB'):
        response: 'Response' = Category().add_category(
            RequestCreateCategory(category=category),
        )
        db_category = db_niffler_spend.get_value(
            'select category from category where id = \'%s\''
            % response.json()['id']
        )[0][0]

        assert response.status_code == HTTPStatus.OK
        response: ResponseCreateCategory = ResponseCreateCategory.model_validate(response.json())
        assert response.username == Configs.TEST_USER
        assert response.category == category == db_category
