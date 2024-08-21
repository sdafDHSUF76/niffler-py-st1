from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.base_logic import BaseLogic
from niffler_e_2_e_tests_python.fixtures.database import db_niffler_spend  # noqa F401
from niffler_e_2_e_tests_python.configs import TEST_USER, TEST_PASSWORD
from niffler_e_2_e_tests_python.presentation.authorization.main.profile.conftest import clear_spend_and_category_before, clear_spend_and_category_after, create_categories

if TYPE_CHECKING:

    from niffler_e_2_e_tests_python.presentation.authorization.login_page import LoginPage
    from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
    from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage


@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestsMain:

    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category1'}},
    )
    @pytest.mark.usefixtures('create_categories', 'goto_main', 'clear_spend_and_category_after')
    def test_create_spend(self, main_page: 'MainPage'):
        main_page.fill(main_page.choose_category, 'category1')
        # main_page.driver.locator(main_page.category_one).press('Enter')
        # expect(main_page.driver.locator(main_page.category_one)).to_be_visible()
        main_page.click(main_page.category_one)
        main_page.fill(main_page.input_number, '1')
        main_page.fill(main_page.spend_date, '19/08/2024')
        main_page.driver.locator(main_page.spend_date).press('Enter')
        main_page.fill(main_page.input_description, 'asdf')
        main_page.click(main_page.button)
        expect(main_page.driver.locator(main_page.spends)).to_have_count(1)


    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'category1'}},
    )
    @pytest.mark.spend_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'spend': {
            "amount": "123",
            "description": "sdff",
            "category": "category1",
            "spendDate": "2024-08-19T19:10:07.256Z",
            "currency": "RUB"
        }},
    )
    @pytest.mark.usefixtures('create_categories', 'create_spends', 'goto_main', 'reload_main_page', 'clear_spend_and_category_after')
    def test_spend_delete(self, main_page: 'MainPage'):
        # main_page.fill(main_page.choose_category, 'category1')
        # main_page.driver.locator(main_page.category_one).press('Enter')
        # expect(main_page.driver.locator(main_page.category_one)).to_be_visible()
        # main_page.click(main_page.category_one)
        # main_page.fill(main_page.input_number, '1')
        # main_page.fill(main_page.spend_date, '19/08/2024')
        # main_page.driver.locator(main_page.spend_date).press('Enter')
        # main_page.fill(main_page.input_description, 'asdf')
        # main_page.click(main_page.button)
        # expect(main_page.driver.locator(main_page.spends)).to_have_count(1)
        # reload_main_page1()
        expect(main_page.driver.locator(main_page.spends)).to_have_count(1)
        main_page.click(main_page.checkbocs_choose_spend)
        main_page.click(main_page.button_delete)
        expect(main_page.driver.locator(main_page.spends)).to_have_count(0)


    @pytest.mark.usefixtures('goto_main', 'reload_main_page1')
    def test_spends_emtpy(self, main_page: 'MainPage'):
        expect(main_page.driver.locator(main_page.spends)).to_have_count(0)

    @pytest.mark.usefixtures('goto_main', 'reload_main_page2')
    def test_categories_emtpy(self, main_page: 'MainPage'):
        main_page.click(main_page.choose_category)
        expect(main_page.driver.locator(main_page.category_one)).to_be_hidden()



