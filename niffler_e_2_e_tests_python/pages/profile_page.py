from typing import TYPE_CHECKING, Optional

import allure

from configs import FRONT_URL
from utils.playwright_helper import PlaywrightHelper
from utils.utils import get_join_url

if TYPE_CHECKING:
    from playwright.sync_api import Page


class ProfilePage(PlaywrightHelper):
    path = '/profile'
    url = get_join_url(FRONT_URL, path)

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.alert_add_category = "//div[@role='alert']"
        self.profile_button = self.driver.locator("//a[@href='/profile']")
        self.alert_add_category_text = self.driver.locator(f"{self.alert_add_category}/div[2]")
        self.alert_button_close = self.driver.locator("//button[@aria-label='close']")
        self.categories_list = self.driver.locator("//ul[@class='categories__list']/li")
        self.categories_input = self.driver.locator("//input[@name='category']")
        self.categories_button = self.driver.locator(
            "//button[@class='button  ' and text()='Create']"
        )
        self.main_button = self.driver.locator("//a[@href='/main']")
        self.subtitle = self.driver.locator('//h2')

    alert_successful_text = 'New category added'
    alert_unsuccessful_text = 'Can not add new category'

    def add_category(self, name_category: str) -> None:
        """Добавляем категорию трат."""
        self.fill(self.categories_input, name_category)
        self.click(self.categories_button)

    def refresh_page_to_update_categories(self, count: int):
        """Обновить страницу, если количество категорий трат не совпало с ожидаемым.

        Нужно, чтобы бэк новые данные на фронт выдал.
        """
        if self.categories_list.count() != count:
            self.refresh_page()

    def check_number_of_existing_categories(self, expected_quantity: int) -> None:
        """Проверить количество существующих категорий трат."""
        with allure.step('check the number of existing categories with the expected'):
            self.expected_number_of_items(self.categories_list, expected_quantity)

    def check_for_popup_appearance(self) -> None:
        """Проверить, что всплывающее окно появилось."""
        self.check_element_is_visible(self.alert_add_category)

    def check_popup_hiding(self) -> None:
        """Проверить, что всплывающее окно исчезло."""
        self.check_element_is_hidden(self.alert_add_category)

    def check_popup_text(self, text: str) -> None:
        """Проверить текст всплывающего окна, после создания категории трат оно появляется."""
        self.check_text_in_element(self.alert_add_category_text, text)

    def get_values_from_category_sheet(self, text_separator: Optional[str] = None) -> list[str]:
        """Получить значения из листа категорий трат."""
        return self.get_text_in_elements(self.categories_list, text_separator)

    def close_popup(self) -> None:
        """Закрыть Popup."""
        return self.click(self.alert_button_close)

    def check_popup_is_hidden(self) -> None:
        """Проверить скрыт ли Popup создания категории трат."""
        return self.check_element_is_hidden(self.alert_add_category)
