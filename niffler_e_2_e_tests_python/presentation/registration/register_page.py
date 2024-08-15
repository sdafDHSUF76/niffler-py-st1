from niffler_e_2_e_tests_python.base_logic import BaseLogic
from niffler_e_2_e_tests_python.configs import AUTH_URL


class RegisterPage(BaseLogic):
    path = '/register'

    input_username = "//input[@name='username']"
    input_password = "//input[@name='password']"
    input_password_submit = "//input[@name='passwordSubmit']"
    button_sign_up = "//button[@type='submit']"
    text_successful_registered = '//p[text()="Congratulations! You\'ve registered!"]'

    def register_new_user(self, username: str, password: str) -> None:
        self.goto_url(f'{AUTH_URL}{self.path}')
        self.fill(self.input_username, username)
        self.fill(self.input_password, password)
        self.fill(self.input_password_submit, password)
        self.click(self.button_sign_up)
