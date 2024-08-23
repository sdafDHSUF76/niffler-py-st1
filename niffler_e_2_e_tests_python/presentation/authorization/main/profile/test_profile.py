from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import expect

from niffler_e_2_e_tests_python.configs import TEST_PASSWORD, TEST_USER

if TYPE_CHECKING:
    from niffler_e_2_e_tests_python.presentation.authorization.main.profile.profile_page import (
        ProfilePage,
    )


@pytest.mark.usefixtures('clear_spend_and_category_before')
class TestProfile:

    @pytest.mark.usefixtures('goto_profile', 'clear_category', 'close_alert')
    def test_crete_category(self, profile_page: 'ProfilePage'):
        categories_before: int = len(
            profile_page.get_text_in_elements(profile_page.categories_list),
        )
        profile_page.add_category('yio2')
        profile_page.expected_number_of_items(profile_page.categories_list, categories_before + 1)
        categories: list[str] = profile_page.get_text_in_elements(
            profile_page.categories_list, '\n',
        )
        assert 'yio2' in categories

    @pytest.mark.usefixtures('goto_profile', 'clear_category')
    @pytest.mark.parametrize(
        'category', ['yiosdf', '1'], ids=['successful alert', 'unsuccessful alert'],
    )
    def test_alert_disappears_after_it_appears(self, profile_page: 'ProfilePage', category: str):
        profile_page.add_category(category)
        expect(profile_page.driver.locator(profile_page.alert_add_category)).to_be_visible()
        expect(profile_page.driver.locator(profile_page.alert_add_category)).to_be_hidden()

    @pytest.mark.parameter_data(
        {'user': TEST_USER, 'password': TEST_PASSWORD, 'category': {'category': 'yuio'}},
    )
    @pytest.mark.usefixtures(
        'create_categories', 'goto_profile', 'clear_category', 'reload_profile_page',
    )
    def test_do_not_create_non_unique_category(self, profile_page: 'ProfilePage'):
        expect(profile_page.driver.locator(profile_page.categories_list)).to_have_count(1)
        categories: list[str] = profile_page.get_text_in_elements(
            profile_page.categories_list, '\n',
        )
        assert 'yuio' in categories
        profile_page.add_category('yuio')
        profile_page.expected_number_of_items(profile_page.categories_list, 1)
        expect(profile_page.driver.locator(profile_page.alert_add_category)).to_be_visible()
        profile_page.check_text_in_element(
            profile_page.alert_add_category_text, profile_page.alert_unsuccessful_text,
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
        'create_categories', 'goto_profile', 'clear_category', 'reload_profile_page',
    )
    def test_do_not_create_more_than_8_categories(self, profile_page: 'ProfilePage'):
        profile_page.expected_number_of_items(profile_page.categories_list, 8)
        profile_page.add_category('yuio')
        categories: list[str] = profile_page.get_text_in_elements(
            profile_page.categories_list, '\n',
        )
        assert 'yuio' not in categories
        profile_page.expected_number_of_items(profile_page.categories_list, 8)
        expect(profile_page.driver.locator(profile_page.alert_add_category)).to_be_visible()
        profile_page.check_text_in_element(
            profile_page.alert_add_category_text, profile_page.alert_unsuccessful_text,
        )

    @pytest.mark.usefixtures('goto_profile', 'clear_category_before', 'reload_profile_page')
    def test_empty_categories(self, profile_page: 'ProfilePage'):
        profile_page.expected_number_of_items(profile_page.categories_list, 0)
