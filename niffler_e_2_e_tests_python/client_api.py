from typing import TYPE_CHECKING

import allure
import pkce
import requests
from allure_commons.types import AttachmentType

from niffler_e_2_e_tests_python.configs import AUTH_URL, FRONT_URL1, GATEWAY_URL
from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
from niffler_e_2_e_tests_python.presentation.registration.register_page import RegisterPage
from requests_toolbelt.utils.dump import dump_response

if TYPE_CHECKING:
    from requests import Response


class ClientApi:
    """Методы, для работы с клиентом."""

    @staticmethod
    def attach_response(response: 'Response'):
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    requests.Session().hooks["response"].append(attach_response)

    @staticmethod
    def create_user(user_name: str, password: str) -> 'Response':
        """Создать пользователя."""
        cookie: str = '; '.join((
            requests.get(AUTH_URL).history[0].headers['Set-Cookie'].replace(', ', '').split(
                '; Path=/',
            )[:2]
        ))
        return requests.post(
            f'{AUTH_URL}{RegisterPage.path}',
            data=dict(
                _csrf=cookie.split('; ')[0].split('XSRF-TOKEN=')[1],
                username=user_name,
                password=password,
                passwordSubmit=password,
            ),
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie}
        )

    @staticmethod
    def add_spend(data_spend: dict, token: str) -> None:
        """Добавить трату."""
        requests.post(
            f'{GATEWAY_URL}/api/spends/add',
            json=data_spend,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json',
            }
        )

    @staticmethod
    def get_token(user_name: str, password: str) -> str:
        """Получить токен."""
        code_verifier: str = pkce.generate_code_verifier(length=43)
        code_challenge: str = pkce.get_code_challenge(code_verifier)
        response0: 'Response' = requests.get(
            f'{AUTH_URL}/oauth2/authorize?',
            params={
                'response_type': 'code',
                'client_id': 'client',
                'scope': 'openid',
                'redirect_uri': f'{FRONT_URL1}/authorized',
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
            },
        )
        xsrf: str = response0.headers.get('X-XSRF-TOKEN')
        jsessionid1: str = response0.history[0].headers.get('Set-Cookie').split('; Path=/')[0]
        response1: 'Response' = requests.post(
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
            f'{FRONT_URL1}/authorized?code=',
        )[1]
        jsessionid2: str = response1.history[0].headers.get('Set-Cookie').split('; Path=/, ')[0]
        response2: 'Response' = requests.post(
            f'{AUTH_URL}/oauth2/token',
            data={
                'code': url_token,
                'redirect_uri': f'{FRONT_URL1}/authorized',
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