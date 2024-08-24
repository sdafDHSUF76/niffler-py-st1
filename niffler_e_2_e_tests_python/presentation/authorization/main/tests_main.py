from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.configs import FRONT_URL1, TEST_PASSWORD, TEST_USER
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


@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestsMain:

    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category1'}},
    )
    @pytest.mark.usefixtures('create_categories', 'goto_main', 'clear_spend_and_category_after')
    def test_create_spend(self, main_page: 'MainPage'):
        main_page.fill(main_page.category_input, 'category1')
        main_page.click(main_page.category_drop_down_list)
        main_page.fill(main_page.input_number, '1')
        main_page.fill(main_page.spend_date, '19/08/2024')
        main_page.driver.locator(main_page.spend_date).press('Enter')
        main_page.fill(main_page.description_input, 'asdf')
        main_page.click(main_page.create_spend_button)
        main_page.expected_number_of_items(main_page.spends, 1)

    @pytest.fixture
    def refresh_page_when_front_and_spend(self, db_niffler_spend: 'DB', main_page: 'MainPage'):
        categories_in_db: int = db_niffler_spend.get_value(
            'select count(*) from spend where username = \'%s\' and amount  = 123' % TEST_USER
        )[0][0]
        categories_in_front: int = main_page.driver.locator(main_page.spends).count()
        category_text: bool = main_page.driver.locator(main_page.spend_amount).inner_text() == '123'
        if (
            main_page.driver.url == get_join_url(FRONT_URL1, main_page.path)
            and (categories_in_db != categories_in_front or not category_text)
        ):
            main_page.driver.reload()

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
        main_page.expected_number_of_items(main_page.spends, 1)
        main_page.click(main_page.checkbox_choose_spend)
        main_page.click(main_page.button_delete)
        main_page.expected_number_of_items(main_page.spends, 0)

    @pytest.fixture
    def refresh_page_when_front_and_db_spend_are_different(
        self, db_niffler_spend: 'DB', main_page: 'MainPage',
    ):
        categories_in_db: int = db_niffler_spend.get_value(
            'select count(*) from spend where username = \'%s\'' % TEST_USER
        )[0][0]
        categories_in_front: int = main_page.driver.locator(main_page.spends).count()
        if (
            main_page.driver.url == get_join_url(FRONT_URL1, main_page.path)
            and categories_in_db != categories_in_front
        ):
            main_page.driver.reload()

    @pytest.mark.usefixtures('goto_main', 'refresh_page_when_front_and_db_spend_are_different')
    def test_spends_emtpy(self, main_page: 'MainPage'):
        main_page.expected_number_of_items(main_page.spends, 0)

    @pytest.fixture
    def refresh_page_when_front_and_db_category_are_different(
        self, db_niffler_spend: 'DB', main_page: 'MainPage',
    ):
        categories_in_db: int = db_niffler_spend.get_value(
            'select count(*) from category where username = \'%s\'' % TEST_USER
        )[0][0]
        main_page.click(main_page.category_input)
        categories_in_front: int = main_page.driver.locator(
            main_page.category_drop_down_list,
        ).count()
        if (
            main_page.driver.url == get_join_url(FRONT_URL1, main_page.path)
            and categories_in_db != categories_in_front
        ):
            main_page.driver.reload()

    @pytest.mark.usefixtures('goto_main', 'refresh_page_when_front_and_db_category_are_different')
    def test_categories_emtpy(self, main_page: 'MainPage'):
        main_page.click(main_page.category_input)
        expect(main_page.driver.locator(main_page.category_drop_down_list)).to_be_hidden()
