import json
from http import HTTPStatus
from typing import TYPE_CHECKING

from allure import epic, feature, title
from faker import Faker
from test_kafka.enums.Topics import Topics
from test_kafka.models.authorization_data import AuthorizationDataUser
from tests_api.clients_api.user import User

if TYPE_CHECKING:
    from client.kafka_client import KafkaClient
    from confluent_kafka import TopicPartition
    from requests import Response
    from utils.database import DB


@epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
@feature("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку в топи \'users\'")
class TestAuthRegistrationKafkaTest:

    @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
    def test_message_should_be_produced_to_kafka_after_successful_registration(
        self, client_kafka: 'KafkaClient', db_niffler_userdata: 'DB',
    ):
        expected_user_name: str = Faker().user_name()
        password: str = Faker().password(special_chars=False)
        topic_partitions: list['TopicPartition'] = client_kafka.subscribe_listen_new_offsets(
            Topics.USERS.value,
        )

        response: 'Response' = User().create_user(expected_user_name, password)

        assert response.status_code == HTTPStatus.CREATED
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
        assert db_niffler_userdata.get_value(
            'select 1 from "user" where username = \'%s\'' % expected_user_name
        ), (
            f'В базе: \'niffler-userdata\' данных не нашлось совпадений с {expected_user_name} '
            'в столбце username'
        )
