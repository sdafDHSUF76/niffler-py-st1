from typing import TYPE_CHECKING

import allure
import pytest
from configs import Configs

if TYPE_CHECKING:

    from tests_ui.pages.profile_page import ProfilePage
    from utils.database import DB


@pytest.fixture
def close_alert_after(profile_page: 'ProfilePage'):
    """Закрыть popup уведомления после теста."""
    yield
    profile_page.close_popup()
    profile_page.check_popup_is_hidden()


@pytest.fixture
def refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db(
    db_niffler_spend: 'DB', profile_page: 'ProfilePage',
) -> None:
    """Обновить страницу, если количество на фронте категории трат не совпадают с базой данных.

    Это нужно чтобы фикстуры setup делали через api запросы и подготавливали состояние, для
    теста быстро, чтобы через UI не делать те же шаги, но медленнее.
    """
    if profile_page.driver.url == profile_page.url:
        categories_in_db: int = db_niffler_spend.get_value(
            'select count(*) from category where username = \'%s\'' % Configs.TEST_USER
        )[0][0]
        categories_in_front: int = profile_page.categories_list.count()
        if categories_in_db != categories_in_front:
            profile_page.refresh_page()


@pytest.fixture
def close_alert_after(profile_page: 'ProfilePage'):
    yield
    profile_page.close_popup()
    profile_page.check_popup_is_hidden()


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
    @pytest.mark.usefixtures('clear_category', 'goto_profile', 'close_alert_after')
    def test_crete_category(self, profile_page: 'ProfilePage'):
        categories_before: int = len(profile_page.get_values_from_category_sheet())
        profile_page.add_category('yio2')
        profile_page.check_number_of_existing_categories(categories_before + 1)
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yio2' in categories

    @allure.story('an alert is displayed about the success of creating a category')
    @pytest.mark.usefixtures('clear_category', 'goto_profile')
    @pytest.mark.parametrize(
        'category', ['yiosdf', '1'], ids=['successful alert', 'unsuccessful alert'],
    )
    @allure.step
    def test_alert_hides_after_appearing(self, profile_page: 'ProfilePage', category: str):
        profile_page.add_category(category)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_hiding()

    @allure.story(
        'check the uniqueness of categories',
        'create a database table to store spending categories',
    )
    @pytest.mark.parameter_data(
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'yuio'},
        },
    )
    @pytest.mark.usefixtures(
        'clear_category',
        'create_categories',
        'goto_profile',
        'refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db',
    )
    @allure.step
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
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category1'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category2'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category3'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category4'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category5'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category6'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category7'},
        },
        {
            'user': Configs.TEST_USER,
            'password': Configs.TEST_PASSWORD,
            'category': {'category': 'category8'},
        },
    )
    @pytest.mark.usefixtures(
        'clear_category',
        'create_categories',
        'goto_profile',
        'refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db',
    )
    @allure.step
    def test_do_not_create_more_than_8_categories(self, profile_page: 'ProfilePage'):
        profile_page.check_number_of_existing_categories(8)
        profile_page.add_category('yuio')
        categories: list[str] = profile_page.get_values_from_category_sheet('\n')
        assert 'yuio' not in categories
        profile_page.check_number_of_existing_categories(8)
        profile_page.check_for_popup_appearance()
        profile_page.check_popup_text(profile_page.alert_unsuccessful_text)

    @allure.story('create a database table to store spending categories')
    @pytest.mark.usefixtures(
        'clear_category',
        'goto_profile',
        'refresh_page_when_there_are_no_spending_categories_on_front_what_is_in_db',
    )
    @allure.step
    def test_empty_categories(self, profile_page: 'ProfilePage'):
        """Проверяем, по дефолту у нас нету лишних категорий трат, только те, что сами создаем."""
        profile_page.check_number_of_existing_categories(0)
