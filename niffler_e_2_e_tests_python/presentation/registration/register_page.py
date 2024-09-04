from typing import TYPE_CHECKING

import allure

from niffler_e_2_e_tests_python.base_logic import PlaywrightHelper
from niffler_e_2_e_tests_python.configs import AUTH_URL

if TYPE_CHECKING:
    from playwright.sync_api import Page


@allure.epic(
    'Registration page',
    'features (what the user can do) for an unauthorized\\authorized user',
)
@allure.epic('features (what the user can do) for an unauthorized user')
class RegisterPage(PlaywrightHelper):
    path = '/register'

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.input_username = self.driver.locator("//input[@name='username']")
        self.input_password = self.driver.locator("//input[@name='password']")
        self.input_password_submit = self.driver.locator("//input[@name='passwordSubmit']")
        self.button_sign_up = self.driver.locator("//button[@type='submit']")
        self.text_successful_registered = self.driver.locator(
            '//p[text()="Congratulations! You\'ve registered!"]'
        )

    def register_new_user(self, username: str, password: str) -> None:
        """Регистрация пользователя."""
        with allure.step('registering a new user'):
            self.goto_url(f'{AUTH_URL}{self.path}')
            self.fill(self.input_username, username)
            self.fill(self.input_password, password)
            self.fill(self.input_password_submit, password)
            self.click(self.button_sign_up)
