from typing import TYPE_CHECKING

import allure
import pkce
import requests
from allure_commons.types import AttachmentType
from configs import configs
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from requests_toolbelt.utils.dump import dump_response

from tests_api.clients_api.base_api import BaseApi
from tests_api.clients_api.enums import HttpMethods

if TYPE_CHECKING:
    from requests import Response, Session


class AuthorizationApi(BaseApi):
    def __init__(self, base_url: str = configs['AUTH_URL']):
        super().__init__(base_url)

    def create_user(self, user_name: str, password: str) -> 'Response':
        """Создать пользователя."""
        cookie: str = '; '.join((
            self.request(HttpMethods.GET, '/').history[0].headers['Set-Cookie'].replace(
                ', ', ''
            ).split('; Path=/')[:2]
        ))
        return self.request(
            HttpMethods.POST,
            f'{RegisterPage.path}',
            data=dict(
                _csrf=cookie.split('; ')[0].split('XSRF-TOKEN=')[1],
                username=user_name,
                password=password,
                passwordSubmit=password,
            ),
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie},
        )

    def get_token(self, user_name: str, password: str) -> str:
        """Получить токен."""
        code_verifier: str = pkce.generate_code_verifier(length=43)
        code_challenge: str = pkce.get_code_challenge(code_verifier)
        response0: 'Response' = self.request(
            HttpMethods.GET,
            '/oauth2/authorize?',
            params={
                'response_type': 'code',
                'client_id': 'client',
                'scope': 'openid',
                'redirect_uri': f'{configs["FRONT_URL"]}/authorized',
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
            },
        )
        xsrf: str = response0.headers.get('X-XSRF-TOKEN')
        jsessionid1: str = response0.history[0].headers.get('Set-Cookie').split('; Path=/')[0]
        response1: 'Response' = self.request(
            HttpMethods.POST,
            f'{LoginPage.path}',
            data={'_csrf': xsrf, 'username': user_name, 'password': password},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': '; XSRF-TOKEN='.join((jsessionid1, xsrf)),
            },
        )
        url_token: str = response1.history[1].headers.get('Location').split(
            f'{configs["FRONT_URL"]}/authorized?code=',
        )[1]
        jsessionid2: str = response1.history[0].headers.get('Set-Cookie').split('; Path=/, ')[0]
        response2: 'Response' = self.request(
            HttpMethods.POST,
            '/oauth2/token',
            data={
                'code': url_token,
                'redirect_uri': f'{configs["FRONT_URL"]}/authorized',
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


class ClientApi(BaseApi):
    """Методы, для работы с клиентом."""

    def __init__(self, base_url: str = configs['FRONT_URL']):
        super().__init__(base_url)


