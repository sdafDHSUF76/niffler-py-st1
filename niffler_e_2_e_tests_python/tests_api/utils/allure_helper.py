import json
import logging
from json import JSONDecodeError
from typing import TYPE_CHECKING

import allure
import curlify as curlify
from allure_commons.types import AttachmentType

if TYPE_CHECKING:
    from requests import Response


def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент и в консоль."""
    def wrapper(*args, **kwargs):
        method, url = args[1].name, args[2]
        with allure.step(f"{method} {url}"):

            response: 'Response' = function(*args, **kwargs)

            curl: str = curlify.to_curl(response.request)
            logging.debug(curl)
            logging.debug(response.text)

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
                    extension=".txt")
            allure.attach(
                body=json.dumps(dict(response.headers), indent=4).encode("utf8"),
                name=f"Response headers {response.status_code}",
                attachment_type=AttachmentType.JSON,
                extension=".json"
            )
        return response

    return wrapper
