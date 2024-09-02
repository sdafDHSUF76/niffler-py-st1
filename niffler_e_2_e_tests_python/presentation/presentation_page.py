import allure

from niffler_e_2_e_tests_python.base_logic import BaseLogic


class PresentationPage(BaseLogic):
    button_login = "//a[text()='Login']"
    button_register = "//a[text()='Register']"

    @allure.step('Check the visibility of the Login button')
    def check_visibility_of_login_button(self):
        self.check_element_is_visible(self.button_login)

    @allure.step('Check the visibility of the Register button')
    def check_visibility_of_register_button(self):
        self.check_element_is_visible(self.button_register)
