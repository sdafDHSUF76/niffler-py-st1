from typing import TYPE_CHECKING

import allure

from configs import AUTH_URL
from utils.playwright_helper import PlaywrightHelper
from utils.utils import get_join_url

if TYPE_CHECKING:
    from playwright.sync_api import Page


class RegisterPage(PlaywrightHelper):
    path = '/register'
    url = get_join_url(AUTH_URL, path)

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.input_username = self.driver.locator("//input[@name='username']")
        self.input_password = self.driver.locator("//input[@name='password']")
        self.input_password_submit = self.driver.locator("//input[@name='passwordSubmit']")
        self.button_sign_up = self.driver.locator("//button[@type='submit']")
        self.text_successful_registered = self.driver.locator(
            '//p[text()="Congratulations! You\'ve registered!"]'
        )

    def register_user(self, username: str, password: str) -> None:
        """Регистрация пользователя."""
        with allure.step('registering a new user'):
            self.goto_your_page()
            self.fill(self.input_username, username)
            self.fill(self.input_password, password)
            self.fill(self.input_password_submit, password)
            self.click(self.button_sign_up)
