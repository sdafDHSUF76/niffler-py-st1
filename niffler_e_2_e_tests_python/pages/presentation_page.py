from typing import TYPE_CHECKING

import allure
from configs import configs
from utils.playwright_helper import PlaywrightHelper

if TYPE_CHECKING:
    from playwright.sync_api import Page


class PresentationPage(PlaywrightHelper):
    url = configs['FRONT_URL']

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.button_login = self.driver.locator("//a[text()='Login']")
        self.button_register = self.driver.locator("//a[text()='Register']")

    @allure.step('Check the visibility of the Login button')
    def check_visibility_of_login_button(self):
        """Проверить видимо кнопки логина."""
        self.check_element_is_visible(self.button_login)

    @allure.step('Check the visibility of the Register button')
    def check_visibility_of_register_button(self):
        """Проверить видимо кнопки регистрации."""
        self.check_element_is_visible(self.button_register)

    @allure.step('click on the Login button')
    def click_on_login_button(self):
        """Нажать на Login кнопку."""
        self.click(self.button_login)
