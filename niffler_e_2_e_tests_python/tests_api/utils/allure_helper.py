import json
from json import JSONDecodeError
from typing import TYPE_CHECKING

import allure
import curlify as curlify
import structlog
from allure_commons.types import AttachmentType

if TYPE_CHECKING:
    from requests import Response

logger = structlog.get_logger('requests')


def allure_attach_request(function):
    """Логируем в allure логи запросов и ответов.

    Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент
    и в консоль.
    """
    def wrapper(
        *unnamed_fields_of_api_request_from_method,
        **named_fields_of_api_request_from_method,
    ):
        method, url = (
            unnamed_fields_of_api_request_from_method[1].name,
            unnamed_fields_of_api_request_from_method[2]
        )
        with allure.step(f"{method} {url}"):

            response: 'Response' = function(
                *unnamed_fields_of_api_request_from_method,
                **named_fields_of_api_request_from_method
            )

            curl: str = curlify.to_curl(response.request)
            logger.debug('request\t', curl=curl)
            logger.debug('response header\t', body=response.headers)
            logger.debug('response body\t', body=response.text)
            # logging.debug(curl) #не понял, как работает, но оставлю
            # logging.debug(response.text)

            allure.attach(
                body=curlify.to_curl(response.request).encode("utf8"),
                name=f"Request {response.status_code}",
                attachment_type=AttachmentType.TEXT,
                extension=".txt"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".json"
                )
            except JSONDecodeError:
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt"
                )
            allure.attach(
                body=json.dumps(dict(response.headers), indent=4).encode("utf8"),
                name=f"Response headers {response.status_code}",
                attachment_type=AttachmentType.JSON,
                extension=".json"
            )
        return response

    return wrapper
