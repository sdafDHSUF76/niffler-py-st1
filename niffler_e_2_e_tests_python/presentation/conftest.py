import re
from typing import TYPE_CHECKING, Callable

import pkce
import pytest
import requests
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.configs import FRONT_URL1, AUTH_URL
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage
from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage

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
def go_login_page(presentation_page: PresentationPage, main_page: 'MainPage') -> None:
    """Это костыль, благодаря которому приложение дает авторизоваться.

    проблема не в автотесте, а в самом приложении, не дает авторизоваться если напрямую перети по
    /login. Выдает ошибку.
    И таких мест, где странное поведение происходит еще нашел 2. При регистрации нового пользователя
    в username если вводить неправильные данные, то текст ошибки разный каждый раз...
    При создании нового пользоватля и авторизации через него, и сделать так несколько раз, то на
    второй раз приложение не даст войти и придется 4 раза на login нажимать, чтобы на login страницу
    перешли...
    """

    if (
        main_page.driver.locator(main_page.profile).is_visible()
        and main_page.driver.url != f'{AUTH_URL}/login'
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
        presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)


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
def logout(main_page: 'MainPage'):
    """Выходим из под учетки юзера."""
    yield
    main_page.click_logout()


@pytest.fixture
def clear_storage(driver: 'Page'):
    """Чистим Storage."""
    yield
    driver.evaluate("() => sessionStorage.clear()")
    driver.evaluate("() => localStorage.clear()")


# @pytest.mark.usefixtures('go_login_page')
@pytest.fixture
def get_token(login_page: 'LoginPage', main_page: 'MainPage', presentation_page: PresentationPage) -> Callable[[str, str], str]:
    """Получаем Bearer токен, для api запросов.

    Пришлось делать через браузер, так как через api требуется работа bundle.js, который проставляет
    id_token, codeVerifier, codeChallenge. Api требует в response Это указывая этот bundle.js
    const verifier = (0,_api_utils__WEBPACK_IMPORTED_MODULE_1__.generateCodeVerifier)();
    sessionStorage.setItem('codeVerifier', verifier);
    const codeChallenge = (0,_api_utils__WEBPACK_IMPORTED_MODULE_1__.generateCodeChallenge)();
    sessionStorage.setItem('codeChallenge', codeChallenge);

    ...
    if (data?.id_token) {
          sessionStorage.setItem('id_token', data.id_token);
    """
    code_verifier: str = pkce.generate_code_verifier(length=43)
    code_challenge: str = pkce.get_code_challenge(code_verifier)
    result: 'Response' = requests.get(
        f'{AUTH_URL}/oauth2/authorize?',
        params={
            'response_type': 'code',
            'client_id': 'client',
            'scope': 'openid',
            'redirect_uri': 'http://frontend.niffler.dc/authorized',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'continue': '',
        }
    )
    def _method(user: str, password: str) -> str:
        if main_page.driver.locator(main_page.profile).is_visible():
            main_page.click_logout()
        presentation_page.goto_url(FRONT_URL1)
        presentation_page.click(presentation_page.button_login)
        login_page.authorization(user, password)
        expect(main_page.driver.locator(main_page.header)).to_have_text(main_page.text_header)
        token: str = login_page.driver.evaluate("() => sessionStorage.getItem('id_token')")
        main_page.click_logout()
        return f'Bearer {token}'
    return _method


if __name__ == '__main__':

    code_verifier: str = pkce.generate_code_verifier(length=43)
    code_challenge: str = pkce.get_code_challenge(code_verifier)
    response1: 'Response' = requests.get(
        f'{AUTH_URL}/oauth2/authorize?',
        params={
            'response_type': 'code',
            'client_id': 'client',
            'scope': 'openid',
            'redirect_uri': 'http://frontend.niffler.dc/authorized',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
        },
    )
    xsrf = response1.headers.get('X-XSRF-TOKEN')
    jsessionid1 = response1.history[0].headers.get('Set-Cookie').split('; Path=/')[0]
    # xsrf: str = requests.get(
    #     f'{AUTH_URL}{LoginPage.path}',
    #     headers={'Cookie': jsessionid1},
    # ).headers.get('X-XSRF-TOKEN')
    response: 'Response' = requests.post(
        f'{AUTH_URL}{LoginPage.path}',
        data={
            '_csrf': xsrf,
            'username': 'qwe',
            'password': '123'
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '; XSRF-TOKEN='.join((jsessionid1, xsrf)),
            'Referer': 'http://auth.niffler.dc:9000/login',
            'Origin': 'http://auth.niffler.dc:9000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
          'Upgrade-Insecure-Requests': '1',
           'Priority': 'u=0, i',
                                                                                                                                   'Connection': 'keep-alive'
        },
    )
    url_token: str = response.history[1].headers.get('Location').split('http://frontend.niffler.dc/authorized?code=')[1]
    jsessionid2 = response.history[0].headers.get('Set-Cookie').split('; Path=/, ')[0]


    # responsewer: 'Response' = requests.options(
    #     f'{AUTH_URL}/oauth2/token',
    # )
    # responsewer2: 'Response' = requests.options(
    #     f'{AUTH_URL}/oauth2/token',
    # )
    response2: 'Response' = requests.post(
        f'{AUTH_URL}/oauth2/token',
        data={
            'code': url_token,
            'redirect_uri': 'http://frontend.niffler.dc/authorized',
            'code_verifier': code_verifier,
            'grant_type': "authorization_code",
            'client_id': 'client'
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': jsessionid2,
            'Authorization': 'Basic Y2xpZW50OnNlY3JldA==',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Referer': 'http://frontend.niffler.dc/',
            'Origin': 'http://frontend.niffler.dc',
            'Accept': '*/*',
                                                                                                                                   'Connection': 'keep-alive'
        },
    )

    # result: 'Response' = requests.get(
    #     f'{AUTH_URL}/oauth2/authorize?',
    #     params={
    #         'response_type': 'code',
    #         'client_id': 'client',
    #         'scope': 'openid',
    #         'redirect_uri': 'http://frontend.niffler.dc/authorized',
    #         'code_challenge': code_challenge,
    #         'code_challenge_method': 'S256',
    #         'continue': '',
    #     },
    #     headers={'Cookie': jsessionid}
    #     #'JSESSIONID=B82D6573EB1A1786531D92A0EA739694'
    # # 'JSESSIONID=6E2183CD2B00471606AB83D0850AD5E2'
    # )
    pass