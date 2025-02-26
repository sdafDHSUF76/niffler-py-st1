import json
import time
from typing import TYPE_CHECKING, Callable

import pytest
from allure import epic, feature, title
from faker import Faker
from test_kafka.enums.Topics import Topics

if TYPE_CHECKING:
    from client.kafka_client import KafkaClient
    from utils.database import DB


@epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
@feature("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку в топик \'users\'")
class TestAuthRegistrationKafkaTest:

    @pytest.fixture
    def get_appearance_of_data_in_userdate(self, db_niffler_userdata: 'DB') -> Callable:
        def _method(expected_user_name: str) -> str:
            attempt = 3
            sleep = 2
            for _ in range(attempt):
                if (
                        value := db_niffler_userdata.get_value(
                        'select username from "user" where username = \'%s\'' % expected_user_name
                    )
                ):
                    return value[0][0]
                else:
                    time.sleep(sleep)
            raise AssertionError(
                'В базе: \'niffler-userdata\' данных не нашлось совпадений с'
                f' {expected_user_name} в столбце username'
            )
        return _method

    @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
    def test_message_should_be_produced_to_kafka_after_successful_registration(
        self,
        client_kafka: 'KafkaClient',
        get_appearance_of_data_in_userdate: Callable,
    ):
        expected_user_name: str = Faker().user_name()
        users_data = {'username': expected_user_name}

        client_kafka.producer.produce(
            Topics.USERS.value,
            json.dumps(users_data).encode('utf-8'),
            headers={'__TypeId__': 'guru.qa.niffler.model.UserJson'},
        )

        current_user_name = get_appearance_of_data_in_userdate(expected_user_name)
        assert current_user_name == expected_user_name, (
            'В базе: \'niffler-userdata\' в столбце username находятся данные: '
            f'{current_user_name}, что не совпали с'
            f'ожидаемыми: {expected_user_name}.'
        )
