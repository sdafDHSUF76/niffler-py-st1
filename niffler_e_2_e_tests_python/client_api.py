from typing import TYPE_CHECKING

import allure
import pkce
import requests
from allure_commons.types import AttachmentType
from requests_toolbelt.utils.dump import dump_response

from niffler_e_2_e_tests_python.configs import AUTH_URL, FRONT_URL, GATEWAY_URL
from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
from niffler_e_2_e_tests_python.presentation.registration.register_page import RegisterPage

if TYPE_CHECKING:
    from requests import Response, Session


class ClientApi:
    """Методы, для работы с клиентом."""

    def __init__(self):
        self.request: Session = requests.session()
        self.request.hooks["response"].append(self.attach_response)

    @staticmethod
    def attach_response(response: 'Response', *args, **kwargs):
        """Приаттачить request, response к шагу, где происходит запрос.

        *args, **kwargs обязательны, так как в этот метод hook передает свои параметры, и если их не
        указать, то метод будет падать, от избытка полученных параметров.
        """
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    def create_user(self, user_name: str, password: str) -> 'Response':
        """Создать пользователя."""
        cookie: str = '; '.join((
            self.request.get(AUTH_URL).history[0].headers['Set-Cookie'].replace(', ', '').split(
                '; Path=/',
            )[:2]
        ))
        return self.request.post(
            f'{AUTH_URL}{RegisterPage.path}',
            data=dict(
                _csrf=cookie.split('; ')[0].split('XSRF-TOKEN=')[1],
                username=user_name,
                password=password,
                passwordSubmit=password,
            ),
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie},
        )

    def add_spend(self, data_spend: dict, token: str) -> None:
        """Добавить трату."""
        self.request.post(
            f'{GATEWAY_URL}/api/spends/add',
            json=data_spend,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json',
            }
        )

    def add_category(self, data_category: dict, token: str) -> None:
        """Добавить трату."""
        self.request.post(
            f'{GATEWAY_URL}/api/categories/add',
            json=data_category,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json',
            }
        )

    def get_token(self, user_name: str, password: str) -> str:
        """Получить токен."""
        code_verifier: str = pkce.generate_code_verifier(length=43)
        code_challenge: str = pkce.get_code_challenge(code_verifier)
        response0: 'Response' = self.request.get(
            f'{AUTH_URL}/oauth2/authorize?',
            params={
                'response_type': 'code',
                'client_id': 'client',
                'scope': 'openid',
                'redirect_uri': f'{FRONT_URL}/authorized',
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
            },
        )
        xsrf: str = response0.headers.get('X-XSRF-TOKEN')
        jsessionid1: str = response0.history[0].headers.get('Set-Cookie').split('; Path=/')[0]
        response1: 'Response' = self.request.post(
            f'{AUTH_URL}{LoginPage.path}',
            data={
                '_csrf': xsrf,
                'username': user_name,
                'password': password,
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': '; XSRF-TOKEN='.join((jsessionid1, xsrf)),
            },
        )
        url_token: str = response1.history[1].headers.get('Location').split(
            f'{FRONT_URL}/authorized?code=',
        )[1]
        jsessionid2: str = response1.history[0].headers.get('Set-Cookie').split('; Path=/, ')[0]
        response2: 'Response' = self.request.post(
            f'{AUTH_URL}/oauth2/token',
            data={
                'code': url_token,
                'redirect_uri': f'{FRONT_URL}/authorized',
                'code_verifier': code_verifier,
                'grant_type': "authorization_code",
                'client_id': 'client'
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': jsessionid2,
                'Authorization': 'Basic Y2xpZW50OnNlY3JldA==',
            },
        )
        return ' '.join(
            (response2.json().get('token_type'), response2.json().get('access_token'))
        )
