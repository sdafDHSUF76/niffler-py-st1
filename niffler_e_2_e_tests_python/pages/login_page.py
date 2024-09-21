from typing import TYPE_CHECKING

import allure
from configs import AUTH_URL
from pages.presentation_page import PresentationPage
from utils.playwright_helper import PlaywrightHelper
from utils.utils import get_join_url

if TYPE_CHECKING:
    from playwright.sync_api import Page


class LoginPage(PlaywrightHelper):
    path = '/login'
    url = get_join_url(AUTH_URL, path)

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
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

    @allure.step('Go to the authorization page and log in')
    def goto_login_page_and_log_in(self, username: str, password: str) -> None:
        """Перейти на страницу авторизации и авторизоваться.

        Эти шаги повторяются, поэтому вынес в отдельный метод.
        """
        self.goto_url(AUTH_URL)
        PresentationPage(self.driver).click_on_login_button()
        self.authorization(username, password)
