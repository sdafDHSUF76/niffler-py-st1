import re
from typing import TYPE_CHECKING, Callable

import pkce
import pytest
import requests

from niffler_e_2_e_tests_python.configs import AUTH_URL, FRONT_URL1
from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage
from niffler_e_2_e_tests_python.utils import get_join_url

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from requests import Response

    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage


@pytest.fixture(scope='class')
def presentation_page(driver: 'Page') -> PresentationPage:
    """Получаем страницу Presentation со всей логикой ее.

    Эта страница, что по этому url Находится http://frontend.niffler.dc
    """
    return PresentationPage(driver)


@pytest.fixture
def go_login_page(
    presentation_page: PresentationPage,
    main_page: 'MainPage',
    go_login_page_function: Callable[[], None],
) -> None:
    """Перейти на страницу авторизации.

    Это костыль, благодаря которому приложение дает авторизоваться.
    Проблема не в автотесте, а в самом приложении, не дает авторизоваться если напрямую перети по
    /login. Выдает ошибку.
    И таких мест, где странное поведение происходит еще нашел 2. При регистрации нового пользователя
    в username если вводить неправильные данные, то текст ошибки разный каждый раз...
    При создании нового пользоватля и авторизации через него, и сделать так несколько раз, то на
    второй раз приложение не даст войти и придется 4 раза на login нажимать, чтобы на login страницу
    перешли...
    """
    if (
        main_page.driver.locator(main_page.profile).is_visible()
        and main_page.driver.url != get_join_url(AUTH_URL, LoginPage.path)
    ):
        main_page.click_logout()
        presentation_page.click(presentation_page.button_login)
    if not re.match('http:\/\/auth\.niffler\.dc:9000\/login', presentation_page.driver.url):  # noqa W605
        """
        Выглядит странным, но у приложения, когда возникает ошибка авторизации в параметре
        url появляется ?error , вроде такой был, и чтобы у меня автотест лишний раз по url не
        переходил у параметризованного теста, то
        вот такая реализация сделана была, где если часть url совпадает , с этим, то переходить на
        url авторизации не нужно, это и быстрее для теста и параметризацию не ломает
        """
        go_login_page_function()


@pytest.fixture
def go_login_page_function(presentation_page: PresentationPage) -> Callable[[], None]:
    """Позволяет авторизоваться, это особенность приложения, что авторизовываемся через такие шаги.

    Такие шаги нужны, после того, как создали пользователя.
    """
    def _method():
        presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)
    return _method


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
