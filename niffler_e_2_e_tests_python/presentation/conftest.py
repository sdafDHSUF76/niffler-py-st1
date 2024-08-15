import re
from typing import TYPE_CHECKING, Callable

import pytest

from niffler_e_2_e_tests_python.configs import FRONT_URL1
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage


@pytest.fixture(scope='class')
def presentation_page(driver: 'Page') -> PresentationPage:
    """Получаем страницу Presentation со всей логикой ее.

    Эта страница, что по этому url Находится http://frontend.niffler.dc
    """
    return PresentationPage(driver)


@pytest.fixture
def go_login_page(presentation_page: PresentationPage):
    """Это костыль, благодаря которому приложение дает авторизоваться.

    проблема не в автотесте, а в самом приложении, не дает авторизоваться если напрямую перети по
    /login. Выдает ошибку.
    И таких мест, где странное поведение происходит еще нашел 2. При регистрации нового пользователя
    в username если вводить неправильные данные, то текст ошибки разный каждый раз...
    При создании нового пользоватля и авторизации через него, и сделать так несколько раз, то на
    второй раз приложение не даст войти и придется 4 раза на login нажимать, чтобы на login страницу
    перешли...
    """
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
    main_page.click(main_page.logout)


@pytest.fixture
def clear_storage(driver: 'Page'):
    """Чистим Storage."""
    yield
    driver.evaluate("() => sessionStorage.clear()")
    driver.evaluate("() => localStorage.clear()")
