from niffler_e_2_e_tests_python.base_logic import BaseLogic


class MainPage(BaseLogic):
    path = '/main'

    header = '//h1'
    logout = "//button[contains(@class,'button-icon_type_logout')]"
    profile = "//a[@href='/profile']"
    main = "//a[@href='/main']"
    choose_category = "//form[@class='add-spending__form']//div[@class=' css-1dx5uak']"
    category_one = "//div[@role='option']"
    input_number = "//input[@type='number']"
    spend_date = "//div[contains(@class,'datepicker')]/input[@type='text']"
    input_description = "//input[@class='form__input ' and @type='text']"
    button = "//button[@type='submit']"
    spends = "//tbody/tr"
    checkbocs_choose_spend = "//td/input[@type='checkbox']"
    button_delete = "//section[@class='spendings__bulk-actions']/button"

    text_header = 'Niffler. The coin keeper.'

    def click_logout(self):
        """Выход из аккаунта через UI."""
        self.click(self.logout)

    # def choose_spending_category(self, category: str) -> None:
    #     self.driver.locator(self.choose_category).select_option(category)
