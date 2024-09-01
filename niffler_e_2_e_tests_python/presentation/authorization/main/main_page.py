from niffler_e_2_e_tests_python.base_logic import BaseSimplifyingLogic


class MainPage(BaseSimplifyingLogic):
    path = '/main'

    header = '//h1'
    logout_button = "//button[contains(@class,'button-icon_type_logout')]"
    profile_button = "//a[@href='/profile']"
    main = "//a[@href='/main']"
    category_input = "//form[@class='add-spending__form']//div[@class=' css-1dx5uak']"
    category_drop_down_list = "//div[@role='option']"
    input_number = "//input[@type='number']"
    spend_date = "//div[contains(@class,'datepicker')]/input[@type='text']"
    description_input = "//input[@class='form__input ' and @type='text']"
    create_spend_button = "//button[@type='submit']"
    spends = "//tbody/tr"
    spend_amount = '//tbody/tr/td[3]//span'
    checkbox_choose_spend = "//td/input[@type='checkbox']"
    button_delete = "//section[@class='spendings__bulk-actions']/button"

    text_header = 'Niffler. The coin keeper.'

    def click_logout(self):
        """Выход из аккаунта через UI."""
        self.click(self.logout_button)
