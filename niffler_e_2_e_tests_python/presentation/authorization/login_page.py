import allure
import re

from niffler_e_2_e_tests_python.base_logic import BaseLogic
from niffler_e_2_e_tests_python.configs import AUTH_URL, FRONT_URL1
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

    @allure.step('we go to the authorization page from different places on the site')
    def goto_login_page(self) -> None:
        """Перейти на страницу авторизации.

            Это костыль, благодаря которому приложение дает авторизоваться.
            Проблема не в автотесте, а в самом приложении, не дает авторизоваться если напрямую
            перети по /login. Выдает ошибку.
            И таких мест, где странное поведение происходит еще нашел 2. При регистрации нового
            пользователя в username если вводить неправильные данные, то текст ошибки разный каждый
            раз...
            При создании нового пользоватля и авторизации через него, и сделать так несколько раз,
            то на второй раз приложение не даст войти и придется 4 раза на login нажимать, чтобы на
            login страницу перешли...
            """
        if (
            self.driver.locator(MainPage.profile_button).is_visible()
            and self.driver.url != get_join_url(AUTH_URL, self.path)
        ):
            MainPage(self.driver).click_logout()
            PresentationPage(self.driver).click(PresentationPage.button_login)
        if not re.match(f'{AUTH_URL}{self.path}', self.driver.url):  # noqa W605
            """
            Выглядит странным, но у приложения, когда возникает ошибка авторизации в параметре
            url появляется ?error , вроде такой был, и чтобы у меня автотест лишний раз по url не
            переходил у параметризованного теста, то
            вот такая реализация сделана была, где если часть url совпадает , с этим, то переходить
            на url авторизации не нужно, это и быстрее для теста и параметризацию не ломает
            """
            PresentationPage(self.driver).goto_url(FRONT_URL1)
            PresentationPage(self.driver).click(PresentationPage.button_login)

    def check_hint_text(self, text: str):
        """Проверить текст подсказки."""
        with allure.step('Checking the hint message'):
            self.check_text_in_element(self.text_error, text)
