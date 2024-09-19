from typing import TYPE_CHECKING

import pytest
from configs import configs
from pages.profile_page import ProfilePage

if TYPE_CHECKING:

    from utils.database import DB


@pytest.fixture
def clear_category_after(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category после теста."""
    yield
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_category_after(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category после теста."""
    yield
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def close_alert_after(profile_page: 'ProfilePage'):
    """Закрыть popup уведомления после теста."""
    yield
    profile_page.close_popup()
    profile_page.check_popup_is_hidden()


@pytest.fixture
def refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db(
    db_niffler_spend: 'DB', profile_page: ProfilePage,
) -> None:
    """Обновить страницу, если количество на фронте категории трат не совпадают с базой данных.

    Это нужно чтобы фикстуры setup делали через api запросы и подготавливали состояние, для
    теста быстро, чтобы через UI не делать те же шаги, но медленнее.
    """
    if profile_page.driver.url == profile_page.url:
        categories_in_db: int = db_niffler_spend.get_value(
            'select count(*) from category where username = \'%s\'' % configs['TEST_USER']
        )[0][0]
        categories_in_front: int = profile_page.categories_list.count()
        if categories_in_db != categories_in_front:
            profile_page.refresh_page()


@pytest.fixture
def close_alert_after(profile_page: ProfilePage):
    yield
    profile_page.close_popup()
    profile_page.check_popup_is_hidden()


@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestProfile:

    @pytest.mark.usefixtures('goto_profile', 'clear_category_after', 'close_alert_after')
    def test_crete_category(self, profile_page: 'ProfilePage'):
        categories_before: int = len(profile_page.get_values_from_category_sheet())
        profile_page.add_category('yio2')
        profile_page.check_number_of_existing_categories(categories_before + 1)
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yio2' in categories

    @pytest.mark.usefixtures('goto_profile', 'clear_category_after')
    @pytest.mark.parametrize(
        'category', ['yiosdf', '1'], ids=['successful alert', 'unsuccessful alert'],
    )
    def test_alert_disappears_after_it_appears(self, profile_page: 'ProfilePage', category: str):
        profile_page.add_category(category)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_hiding()

    @pytest.mark.parameter_data(
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'yuio'},
        },
    )
    @pytest.mark.usefixtures(
        'create_categories',
        'goto_profile',
        'clear_category_after',
        'refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db',
    )
    def test_do_not_create_non_unique_category(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(1)
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yuio' in categories
        profile_page.add_category('yuio')
        profile_page.check_number_of_existing_categories(1)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_text(profile_page.alert_unsuccessful_text)

    @pytest.mark.parameter_data(
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category1'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category2'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category3'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category4'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category5'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category6'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category7'},
        },
        {
            'user': configs['TEST_USER'],
            'password': configs['TEST_PASSWORD'],
            'category': {'category': 'category8'},
        },
    )
    @pytest.mark.usefixtures(
        'create_categories',
        'goto_profile',
        'clear_category_after',
        'refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db',
    )
    def test_do_not_create_more_than_8_categories(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(8)
        profile_page.add_category('yuio')
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yuio' not in categories
        profile_page.check_number_of_existing_categories(8)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_text(profile_page.alert_unsuccessful_text)

    @pytest.mark.usefixtures(
        'goto_profile',
        'clear_category_before',
        'refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db',
    )
    def test_empty_categories(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(0)
