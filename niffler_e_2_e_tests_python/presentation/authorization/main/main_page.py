from niffler_e_2_e_tests_python.base_logic import BaseLogic


class MainPage(BaseLogic):
    path = '/main'

    header = '//h1'
    logout = "//button[contains(@class,'button-icon_type_logout')]"
    profile = "//a[@href='/profile']"

    text_header = 'Niffler. The coin keeper.'

    def click_logout(self):
        """Выход из аккаунта через UI."""
        self.click(self.logout)
