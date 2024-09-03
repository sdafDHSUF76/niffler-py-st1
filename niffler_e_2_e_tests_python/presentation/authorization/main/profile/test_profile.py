from typing import TYPE_CHECKING

import allure
import pytest

from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER, FRONT_URL
from niffler_e_2_e_tests_python.utils import get_join_url

from niffler_e_2_e_tests_python.presentation.authorization.main.profile.profile_page import (
    ProfilePage,
)
if TYPE_CHECKING:

    from niffler_e_2_e_tests_python.fixtures.database import DB

@pytest.fixture
def clear_category_after(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    yield
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_category_before(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    db_niffler_spend.execute('delete from category')

@pytest.fixture
def clear_category_after(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category."""
    yield
    db_niffler_spend.execute('delete from category')

@pytest.fixture
def close_alert_after(profile_page: 'ProfilePage'):
    yield
    profile_page.click(profile_page.alert_button_close)


@pytest.fixture
def reload_profile_page(db_niffler_spend: 'DB', profile_page: ProfilePage):
    """Обновить страницу, если данные на фронте не совпадают с базой данных."""
    if profile_page.driver.url == get_join_url(FRONT_URL, ProfilePage.path):
        categories_in_db: int = db_niffler_spend.get_value(
            'select count(*) from category where username = \'%s\'' % TEST_USER
        )[0][0]
        categories_in_front: int = profile_page.get_element(
            profile_page.categories_list,
        ).count()
        if categories_in_db != categories_in_front:
            profile_page.refresh_page()


@pytest.fixture
def close_alert_after(profile_page: ProfilePage):
    yield
    profile_page.click(profile_page.alert_button_close)



@allure.epic(
    'Profile page',
    'features (what the user can do) for an unauthorized\\authorized user',
)
@allure.feature(
    'features (what the user can do) for an authorized user',
    'Creating a form for creating spending categories',
)
@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestProfile:

    @allure.story(
        'the form of category creations',
        'create a database table to store spending categories',
    )
    @pytest.mark.usefixtures('goto_profile', 'clear_category_after', 'close_alert_after')
    def test_crete_category(self, profile_page: 'ProfilePage'):
        categories_before: int = len(profile_page.get_values_from_category_sheet())
        profile_page.add_category('yio2')
        profile_page.check_number_of_existing_categories(categories_before + 1)
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yio2' in categories

    @allure.story('an alert is displayed about the success of creating a category')
    @pytest.mark.usefixtures('goto_profile', 'clear_category_after')
    @pytest.mark.parametrize(
        'category', ['yiosdf', '1'], ids=['successful alert', 'unsuccessful alert'],
    )
    def test_alert_disappears_after_it_appears(self, profile_page: 'ProfilePage', category: str):
        profile_page.add_category(category)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_hiding()

    @allure.story(
        'check the uniqueness of categories',
        'create a database table to store spending categories',
    )
    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'yuio'}},
    )
    @pytest.mark.usefixtures(
        'create_categories', 'goto_profile', 'clear_category_after', 'reload_profile_page',
    )
    def test_do_not_create_non_unique_category(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(1)
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yuio' in categories
        profile_page.add_category('yuio')
        profile_page.check_number_of_existing_categories(1)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_text(profile_page.alert_unsuccessful_text)

    @allure.story(
        'the limit in the number of created categories is no more than 8',
        'create a database table to store spending categories',
    )
    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category1'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category2'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category3'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category4'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category5'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category6'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category7'}},
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category8'}},
    )
    @pytest.mark.usefixtures(
        'create_categories', 'goto_profile', 'clear_category_after', 'reload_profile_page',
    )
    def test_do_not_create_more_than_8_categories(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(8)
        profile_page.add_category('yuio')
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yuio' not in categories
        profile_page.check_number_of_existing_categories(8)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_text(profile_page.alert_unsuccessful_text)

    @allure.story('create a database table to store spending categories')
    @pytest.mark.usefixtures('goto_profile', 'clear_category_before', 'reload_profile_page')
    def test_empty_categories(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(0)
