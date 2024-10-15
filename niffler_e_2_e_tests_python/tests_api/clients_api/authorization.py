from typing import TYPE_CHECKING

import pkce
from configs import Configs
from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods
from tests_api.utils.base_logic_api import BaseLogicApi

if TYPE_CHECKING:
    from requests import Response


class Authorization(BaseLogicApi):
    """API логика, для авторизации."""
    def __init__(self, base_url: str = None):

        self.base_url = base_url or Configs.AUTH_URL
        super().__init__(self.base_url)

    def get_token(self, user_name: str, password: str) -> str:
        """Получить токен."""
        code_verifier: str = pkce.generate_code_verifier(length=43)
        code_challenge: str = pkce.get_code_challenge(code_verifier)
        response0: 'Response' = self.request(
            HttpMethods.GET,
            f'{PathUrl.OAUTH2_AUTHORIZATION}?',
            params={
                'response_type': 'code',
                'client_id': 'client',
                'scope': 'openid',
                'redirect_uri': f'{Configs.FRONT_URL}{PathUrl.AUTHORIZATION}',
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256',
            },
        )
        xsrf: str = response0.headers.get('X-XSRF-TOKEN')
        jsessionid1: str = response0.history[0].headers.get('Set-Cookie').split('; Path=/')[0]
        response1: 'Response' = self.request(
            HttpMethods.POST,
            PathUrl.LOGIN,
            data={'_csrf': xsrf, 'username': user_name, 'password': password},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': '; XSRF-TOKEN='.join((jsessionid1, xsrf)),
            },
        )
        url_token: str = response1.history[1].headers.get('Location').split(
            f'{Configs.FRONT_URL}{PathUrl.AUTHORIZATION}?code=',
        )[1]
        jsessionid2: str = response1.history[0].headers.get('Set-Cookie').split('; Path=/, ')[0]
        response2: 'Response' = self.request(
            HttpMethods.POST,
            PathUrl.OAUTH2_TOKEN,
            data={
                'code': url_token,
                'redirect_uri': f'{Configs.FRONT_URL}{PathUrl.AUTHORIZATION}',
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
