from typing import TYPE_CHECKING, Optional

import allure
import pytest
from playwright.sync_api import Locator

from niffler_e_2_e_tests_python.client_api import ClientApi
from niffler_e_2_e_tests_python.configs import FRONT_URL, TEST_PASSWORD, TEST_USER
from niffler_e_2_e_tests_python.fixtures.database import db_niffler_spend  # noqa F401
from niffler_e_2_e_tests_python.presentation.authorization.main.profile.conftest import (  # noqa F401
    clear_spend_and_category_after,
    clear_spend_and_category_before,
    create_categories,
)
from niffler_e_2_e_tests_python.utils import get_join_url

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.fixtures.database import DB
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from _pytest.fixtures import SubRequest
    from _pytest.mark import Mark





@pytest.fixture
def create_spends(request: 'SubRequest'):
    """Создаем категории через API.

    На самом деле тут только через API категория создается, а вот токен берется из UI.
    """
    marker: Optional['Mark'] = request.node.get_closest_marker('spend_data')
    user_old, password_old = None, None
    for unit in marker.args:
        user, password = unit['user'], unit['password']
        if user_old != user and password_old != password:
            token: str = ClientApi().get_token(unit['user'], unit['password'])
        ClientApi().add_spend(unit['spend'], token)
        user_old, password_old = user, password

@allure.epic(
    'Main page',
    'features (what the user can do) for an unauthorized\\authorized user',
)
@allure.feature(
    'features (what the user can do) for an authorized user',
    'Create a UI to create expenses',
)
@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestsCreatingExpenses:

    @allure.story(
        'display the created expenses in the spending history',
        'create a form for selecting and creating expenses',
        'create a database table to store spending categories',
        'create a database table to store your spending history',
    )
    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category1'}},
    )
    @pytest.mark.usefixtures('create_categories', 'goto_main', 'clear_spend_and_category_after')
    def test_create_spend(self, main_page: 'MainPage'):
        main_page.fill_input_category('category1')
        main_page.choose_on_drop_down_list_of_spending_categories()
        main_page.fill_input_amount_of_spending('1')
        main_page.fill_input_spend_date('19/08/2024')
        main_page.press_enter_on_keyboard()
        main_page.fill_input_description('asdf')
        main_page.click_on_spending_creation_button()
        main_page.check_number_of_expenses_in_spending_history(1)

    @pytest.fixture
    def refresh_page_when_front_and_db_category_are_different(
        self, db_niffler_spend: 'DB', main_page: 'MainPage',
    ):
        if main_page.driver.url == get_join_url(FRONT_URL, main_page.path):
            categories_in_db: int = db_niffler_spend.get_value(
                'select count(*) from category where username = \'%s\'' % TEST_USER
            )[0][0]
            main_page.click_on_input_category()
            categories_in_front: int = main_page.get_element(main_page.category_drop_down_list).count()
            if categories_in_db != categories_in_front:
                main_page.refresh_page()

    @allure.story(
        'create a form for selecting and creating expenses',
        'create a database table to store spending categories',
    )
    @pytest.mark.usefixtures('goto_main', 'refresh_page_when_front_and_db_category_are_different')
    def test_categories_empty(self, main_page: 'MainPage'):
        main_page.click_on_input_category()
        main_page.check_that_dropdown_is_empty()


@allure.epic(
    'Main page',
    'features (what the user can do) for an unauthorized\\authorized user',
)
@allure.feature(
    'features (what the user can do) for an authorized user',
    'create a spending history display',
)
@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestHistoryOfSpending:

    @pytest.fixture
    def refresh_page_when_front_and_spend(self, db_niffler_spend: 'DB', main_page: 'MainPage'):
        if main_page.driver.url == get_join_url(FRONT_URL, main_page.path):
            categories_in_db: int = db_niffler_spend.get_value(
                'select count(*) from spend where username = \'%s\' and amount  = 123' % TEST_USER
            )[0][0]
            categories_in_front: int = main_page.driver.locator(main_page.spends).count()
            spending_column: Locator = main_page.get_element(main_page.spend_amount)
            is_amount_spend: bool = False
            if spending_column.is_visible():
                is_amount_spend = spending_column.inner_text() == '123'
            if categories_in_db != categories_in_front or not is_amount_spend:
                main_page.refresh_page()


    @allure.story(
        'allow you to delete expenses from your spending history',
        'create a database table to store your spending history',
    )
    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category1'}},
    )
    @pytest.mark.spend_data(
        {
            'user': TEST_USER,
            'password': TEST_PASSWORD,
            'spend': {
                "amount": "123",
                "description": "sdff",
                "category": "category1",
                "spendDate": "2024-08-19T19:10:07.256Z",
                "currency": "RUB",
            }
        },
    )
    @pytest.mark.usefixtures(
        'create_categories',
        'create_spends',
        'goto_main',
        'refresh_page_when_front_and_spend',
        'clear_spend_and_category_after',
    )
    def test_spend_delete(self, main_page: 'MainPage'):
        main_page.check_number_of_expenses_in_spending_history(1)
        main_page.click_on_checkbox_at_selected_expense()
        main_page.click_on_delete_spending_button()
        main_page.check_number_of_expenses_in_spending_history(0)

    @pytest.fixture
    def refresh_page_when_front_and_db_spend_are_different(
        self, db_niffler_spend: 'DB', main_page: 'MainPage',
    ):
        if main_page.driver.url == get_join_url(FRONT_URL, main_page.path):
            categories_in_db: int = db_niffler_spend.get_value(
                'select count(*) from spend where username = \'%s\'' % TEST_USER
            )[0][0]
            categories_in_front: int = main_page.get_element(main_page.spends).count()
            if categories_in_db != categories_in_front:
                main_page.refresh_page()

    @allure.story(
        'create a form for selecting and creating expenses',
        'create a database table to store your spending history',
    )
    @pytest.mark.usefixtures('goto_main', 'refresh_page_when_front_and_db_spend_are_different')
    def test_spends_emtpy(self, main_page: 'MainPage'):
        main_page.check_number_of_expenses_in_spending_history(0)
