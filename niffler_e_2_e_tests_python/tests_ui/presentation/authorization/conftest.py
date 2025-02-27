import re
from typing import TYPE_CHECKING

import pytest
from tests_ui.pages.login_page import LoginPage

if TYPE_CHECKING:
    from tests_ui.pages.main_page import MainPage
    from tests_ui.pages.presentation_page import PresentationPage


@pytest.fixture
def logout_after(main_page: 'MainPage') -> None:
    """Выходим из под учетки юзера после теста."""
    yield
    if main_page.profile_button.is_visible():
        main_page.click_logout()
        main_page.check_that_you_not_logged_in()


@pytest.fixture
def goto_login_page_if_you_logged_in(
    main_page: 'MainPage', presentation_page: 'PresentationPage',
) -> None:
    if main_page.profile_button.is_visible():
        main_page.click_logout()
        main_page.expect_element(main_page.profile_button).to_be_hidden()
        presentation_page.click_on_login_button()


@pytest.fixture
def goto_login_page_if_you_not_logged_in(
    login_page: 'LoginPage', presentation_page: 'PresentationPage',
) -> None:
    if not re.match(f'{login_page.url}', presentation_page.driver.url):
        """
        Выглядит странным, но у приложения, когда возникает ошибка авторизации в параметре
        url появляется ?error , вроде такой был, и чтобы у меня автотест лишний раз по url не
        переходил у параметризованного теста, то
        вот такая реализация сделана была, где если часть url совпадает , с этим, то переходить
        на url авторизации не нужно, это и быстрее для теста и параметризацию не ломает
        """
        presentation_page.goto_your_page()
        presentation_page.click_on_login_button()


@pytest.fixture
def go_login_page(
    goto_login_page_if_you_logged_in: None, goto_login_page_if_you_not_logged_in: None,
) -> None:
    """Перейти на страницу авторизации."""
    pass
