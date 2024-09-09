from typing import TYPE_CHECKING

import allure

from niffler_e_2_e_tests_python.configs import FRONT_URL
from niffler_e_2_e_tests_python.playwright_helper import PlaywrightHelper
from niffler_e_2_e_tests_python.utils import get_join_url

if TYPE_CHECKING:
    from playwright.sync_api import Page


class MainPage(PlaywrightHelper):
    path = '/main'
    url = get_join_url(FRONT_URL, path)

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.header = self.driver.locator('//h1')
        self.logout_button = self.driver.locator(
            "//button[contains(@class,'button-icon_type_logout')]"
        )
        self.profile_button = self.driver.locator("//a[@href='/profile']")
        self.main = self.driver.locator("//a[@href='/main']")

    text_header = 'Niffler. The coin keeper.'

    def click_logout(self):
        """Выход из аккаунта через UI."""
        self.click(self.logout_button)

    def click_profile_button(self):
        """Нажать на кнопку Профиля."""
        self.click(self.profile_button)

    def click_main_button(self):
        """Нажать на кнопку Профиля."""
        self.click(self.main)

    def check_that_you_not_logged_in(self) -> None:
        """Проверить что вышел из учетки."""
        self.check_element_is_hidden(self.profile_button)

    def check_text_of_page_title(self) -> None:
        """Проверить заголовок страницы."""
        self.check_text_in_element(self.header, self.text_header)
