import json
import time
from typing import TYPE_CHECKING, Callable

import pytest
from allure import epic, feature, title
from faker import Faker
from test_kafka.enums.Topics import Topics
from test_kafka.models.authorization_data import AuthorizationDataUser

if TYPE_CHECKING:
    from client.kafka_client import KafkaClient
    from confluent_kafka import TopicPartition
    from utils.database import DB


@epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
@feature("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку в топик \'users\'")
class TestAuthRegistrationKafkaTest:

    @pytest.fixture
    def check_appearance_of_data_in_userdate(self, db_niffler_userdata: 'DB') -> Callable:
        def _method(expected_user_name: str) -> None:
            attempt = 3
            sleep = 2
            for _ in range(attempt):
                try:
                    assert db_niffler_userdata.get_value(
                        'select 1 from "user" where username = \'%s\'' % expected_user_name
                    )
                    return
                except AssertionError:
                    time.sleep(sleep)
                    continue
            raise AssertionError(
                'В базе: \'niffler-userdata\' данных не нашлось совпадений с'
                f' {expected_user_name} в столбце username'
            )
        return _method

    @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
    def test_message_should_be_produced_to_kafka_after_successful_registration(
        self,
        client_kafka: 'KafkaClient',
        db_niffler_userdata: 'DB',
        check_appearance_of_data_in_userdate: Callable,
    ):
        expected_user_name: str = Faker().user_name()
        topic_partitions: list['TopicPartition'] = client_kafka.subscribe_listen_new_offsets(
            Topics.USERS.value,
        )
        users_data = {'username': expected_user_name}
        client_kafka.producer.produce(
            Topics.USERS.value,
            json.dumps(users_data).encode('utf-8'),
            headers={'__TypeId__': 'guru.qa.niffler.model.UserJson'},
        )
        event: bytes | None = client_kafka.log_msg_and_json(topic_partitions)

        assert event != b'' and event is not None, (
            f'сообщения в kafka нету! Проверьте топик: {Topics.USERS.value}.'
        )
        current_authorization_user: str = AuthorizationDataUser.model_validate(
            json.loads(event.decode('utf8')),
        ).model_dump()['user_name']
        assert current_authorization_user == expected_user_name, (
            f'получили сообщение: {current_authorization_user}  из топика: {Topics.USERS.value} и '
            f'оно не совпало с ожидаемым: {expected_user_name}'
        )
        check_appearance_of_data_in_userdate(expected_user_name)
