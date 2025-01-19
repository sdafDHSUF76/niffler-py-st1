from typing import TYPE_CHECKING

import pkce
from configs import Configs
from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods
from tests_api.utils.base_logic_api import BaseLogicApi

if TYPE_CHECKING:
    from requests import Response


class CreateAuthorizedUser(BaseLogicApi):
    """API логика, для авторизации."""
    def __init__(self, base_url: str = None):

        self.base_url = base_url or Configs.AUTH_URL
        super().__init__(self.base_url)

    def register(self, user_name, password) -> 'Response':
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
        return self.request(
            HttpMethods.POST,
            PathUrl.LOGIN,
            data={'_csrf': xsrf, 'username': user_name, 'password': password},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': '; XSRF-TOKEN='.join((jsessionid1, xsrf)),
            },
            allow_redirects=True
        )
        #
        # self.request(
        #     HttpMethods.GET,
        #     PathUrl.REGISTER,
        #     allow_redirects=True
        # )
        #
        # result = self.request(
        #     HttpMethods.POST,
        #     PathUrl.REGISTER,
        #     data={
        #         "username": username,
        #         "password": password,
        #         "passwordSubmit": password,
        #         "_csrf": self.session.cookies.get("XSRF-TOKEN")
        #     },
        #     allow_redirects=True
        # )
        # return result
