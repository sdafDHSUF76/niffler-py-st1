
from typing import TYPE_CHECKING, Callable

import pkce
import pytest
import requests

from niffler_e_2_e_tests_python.configs import AUTH_URL, FRONT_URL1
from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from requests import Response


@pytest.fixture(scope='session')
def presentation_page(driver: 'Page') -> PresentationPage:
    """Получаем страницу Presentation со всей логикой ее.

    Эта страница, что по этому url Находится http://frontend.niffler.dc
    """
    return PresentationPage(driver)


@pytest.fixture
def goto_presentation_url(presentation_page: PresentationPage) -> None:
    """Перейти на страницу презентации.

    Эта та страница, которая тут http://frontend.niffler.dc
    """
    presentation_page.goto_url(FRONT_URL1)


@pytest.fixture
def get_token() -> Callable[[str, str], str]:
    """Получаем Bearer токен, для api запросов."""
    def _method(user: str, password: str) -> str:
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
                'username': user,
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
        return ' '.join((response2.json().get('token_type'), response2.json().get('access_token')))
    return _method
