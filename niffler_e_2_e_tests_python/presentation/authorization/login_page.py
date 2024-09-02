import allure

from niffler_e_2_e_tests_python.base_logic import BaseLogic


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
