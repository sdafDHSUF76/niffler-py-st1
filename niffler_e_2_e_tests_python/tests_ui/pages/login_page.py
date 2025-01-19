from typing import TYPE_CHECKING

import allure
from configs import Configs
from tests_ui.utils.playwright_helper import PlaywrightHelper
from tests_ui.utils.utils import get_join_url

if TYPE_CHECKING:
    from playwright.sync_api import Page


class LoginPage(PlaywrightHelper):
    path = '/login'

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.url = get_join_url(Configs.AUTH_URL, self.path)
        self.input_username = self.driver.locator("//input[@name='username']")
        self.input_password = self.driver.locator("//input[@name='password']")
        self.button_sign_in = self.driver.locator("//button[@type='submit']")
        self.text_error = self.driver.locator("//p[@class='form__error']")

    @allure.step('authorization')
    def authorization(self, username: str, password: str):
        self.fill(self.input_username, username)
        self.fill(self.input_password, password)
        self.click(self.button_sign_in)

    @allure.step('check the prompt when you entered the user\'s data (username and password)')
    def check_hint_text(self, text: str):
        """Проверить текст подсказки."""
        with allure.step('Checking the hint message'):
            self.check_text_in_element(self.text_error, text)
