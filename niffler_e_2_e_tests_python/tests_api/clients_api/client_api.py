from typing import TYPE_CHECKING

import pkce
from configs import Configs
from tests_api.clients_api.base_api import BaseApi
from tests_api.enums.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods

if TYPE_CHECKING:
    from requests import Response


class AuthorizationApi(BaseApi):
    def __init__(self, base_url: str = Configs.AUTH_URL):
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
            PathUrl.register.value,
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
            f'{PathUrl.oauth2_authorization.value}?',
            params={
                'response_type': 'code',
                'client_id': 'client',
                'scope': 'openid',
                'redirect_uri': f'{Configs.FRONT_URL}{PathUrl.authorization.value}',
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
            },
        )
        xsrf: str = response0.headers.get('X-XSRF-TOKEN')
        jsessionid1: str = response0.history[0].headers.get('Set-Cookie').split('; Path=/')[0]
        response1: 'Response' = self.request(
            HttpMethods.POST,
            PathUrl.login.value,
            data={'_csrf': xsrf, 'username': user_name, 'password': password},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': '; XSRF-TOKEN='.join((jsessionid1, xsrf)),
            },
        )
        url_token: str = response1.history[1].headers.get('Location').split(
            f'{Configs.FRONT_URL}{PathUrl.authorization.value}?code=',
        )[1]
        jsessionid2: str = response1.history[0].headers.get('Set-Cookie').split('; Path=/, ')[0]
        response2: 'Response' = self.request(
            HttpMethods.POST,
            PathUrl.oauth2_token.value,
            data={
                'code': url_token,
                'redirect_uri': f'{Configs.FRONT_URL}{PathUrl.authorization.value}',
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
