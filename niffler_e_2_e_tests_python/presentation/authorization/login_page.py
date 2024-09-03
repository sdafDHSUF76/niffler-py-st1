import allure
import re

from niffler_e_2_e_tests_python.base_logic import BaseLogic
from niffler_e_2_e_tests_python.configs import AUTH_URL, FRONT_URL
from niffler_e_2_e_tests_python.presentation.authorization.main.main_page import MainPage
from niffler_e_2_e_tests_python.presentation.presentation_page import PresentationPage
from niffler_e_2_e_tests_python.utils import get_join_url


class LoginPage(BaseLogic):
    path = '/login'

    input_username = "//input[@name='username']"
    input_password = "//input[@name='password']"
    button_sign_in = "//button[@type='submit']"
    text_error = "//p[@class='form__error']"

    @allure.step('authorization')
    def authorization(self, username: str, password: str):
        self.fill(self.input_username, username)
        self.fill(self.input_password, password)
        self.click(self.button_sign_in)





    def check_hint_text(self, text: str):
        """Проверить текст подсказки."""
        with allure.step('Checking the hint message'):
            self.check_text_in_element(self.text_error, text)

    def goto_login_page_and_log_in(self, username: str, password: str) -> None:
        """Перейти на страницу авторизации и авторизоваться.

        Эти шаги повторяются, поэтому вынес в отдельный метод.
        """
        self.goto_url(AUTH_URL)
        PresentationPage(self.driver).click_on_login_button()
        self.authorization(username, password)


