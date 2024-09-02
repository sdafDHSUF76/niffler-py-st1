from typing import Optional

import allure

from niffler_e_2_e_tests_python.base_logic import BaseLogic


class ProfilePage(BaseLogic):
    path = '/profile'

    alert_add_category = "//div[@role='alert']"
    alert_add_category_text = f"{alert_add_category}/div[2]"
    alert_button_close = "//button[@aria-label='close']"
    categories_list = "//ul[@class='categories__list']/li"
    categories_input = "//input[@name='category']"
    categories_button = "//button[@class='button  ' and text()='Create']"
    main_button = "//a[@href='/main']"
    alert_successful_text = 'New category added'
    alert_unsuccessful_text = 'Can not add new category'
    subtitle = '//h2'

    @allure.step('add a category: \'{name_category}\'')
    def add_category(self, name_category: str) -> None:
        """Добавляем категорию трат."""
        self.fill(self.categories_input, name_category)
        self.click(self.categories_button)

    @allure.step(
        'refresh the page if the number of categories does not match the expected one: '
        '\'{count}\''
    )
    def refresh_page_to_update_categories(self, count: int):
        if self.get_element(self.categories_list).count() != count:
            self.refresh_page()

    def check_number_of_existing_categories(self, expected_quantity: int) -> None:
        with allure.step('check the number of existing categories with the expected'):
            self.expected_number_of_items(self.categories_list, expected_quantity)

    @allure.step('check the appearance of a pop-up window about the result of creating a category')
    def check_for_popup_appearance(self) -> None:
        self.check_element_is_visible(self.alert_add_category)

    @allure.step('check the hiding of a pop-up window about the result of creating a category')
    def check_popup_hiding(self) -> None:
        self.check_element_is_hidden(self.alert_add_category)

    @allure.step('check the text of the pop-up window about the result of creating a category')
    def check_popup_text(self, text: str) -> None:
        self.check_text_in_element(self.alert_add_category_text, text)

    def get_values_from_category_sheet(self, text_separator: Optional[str] = None) -> list[str]:
        return self.get_text_in_elements(self.categories_list, text_separator)
