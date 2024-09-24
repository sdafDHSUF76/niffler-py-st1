from typing import TYPE_CHECKING, Callable

import pytest
from configs import Configs
from tests_ui.pages.main_page import MainPage

if TYPE_CHECKING:
    from tests_ui.pages.presentation_page import PresentationPage
    from utils.database import DB


pytest_plugins = ('fixtures.helper_category')


@pytest.fixture(scope='class')
def clear_spend_and_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category и spend."""
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def goto_main_if_you_logged_in(main_page: MainPage) -> None:
    """Перейти на страницу main если авторизован, но находишься на другой странице."""
    if main_page.main.is_visible() and main_page.driver.url != main_page.url:
        main_page.goto_your_page()


@pytest.fixture
def goto_main_if_you_not_logged_in(
    presentation_page: 'PresentationPage',
    goto_login_page_and_log_in: Callable[[str, str], None],
) -> None:
    """Перейти на страницу main если не авторизован и находишься на разных местах сайта."""
    if presentation_page.driver.url != MainPage.url:
        goto_login_page_and_log_in(Configs.TEST_USER, Configs.TEST_PASSWORD)


@pytest.fixture
def goto_main(goto_main_if_you_logged_in: None, goto_main_if_you_not_logged_in: None) -> None:
    """Перейти на страницу main.

    Так как автотест можно запустить один , или запустить целый модуль, то нельзя знать в какой
    момент пользователь будет еще авторизован во время прохождения предыдущих тестов. Чтобы тест
    что будет иметь в себе эту фикстуру не падал из-за разных тестов до него, что были, то решил
    сделать сборную фикстуру, в которой разделил логику перехода на main страницу, когда
    пользователь авторизован и не авторизован.
    """
    pass
