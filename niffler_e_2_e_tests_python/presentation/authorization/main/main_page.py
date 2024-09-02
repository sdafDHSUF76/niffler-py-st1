import allure

from niffler_e_2_e_tests_python.base_logic import BaseLogic


class MainPage(BaseLogic):
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

    @allure.step('log out of your account')
    def click_logout(self):
        """Выход из аккаунта через UI."""
        self.click(self.logout_button)

    def check_number_of_expenses_in_spending_history(self, expected_quantity: int) -> None:
        with allure.step('check the number of entries in your spending history'):
            self.expected_number_of_items(self.spends, expected_quantity)

    @allure.step('click on the checkbox next to the spending record')
    def click_on_checkbox_at_selected_expense(self) -> None:
        self.click(self.checkbox_choose_spend)

    @allure.step('click on the delete selected expenses button')
    def click_on_delete_spending_button(self) -> None:
        self.click(self.button_delete)

    def fill_input_category(self, text: str) -> None:
        with allure.step('fill in the input text of the category'):
            self.fill(self.category_input, text)

    def fill_input_number(self, text: str) -> None:
        with allure.step('fill in the input text of the number'):
            self.fill(self.input_number, text)

    def fill_input_spend_date(self, text: str) -> None:
        with allure.step('fill in the input text of the spend date'):
            self.fill(self.spend_date, text)

    def fill_input_description(self, text: str) -> None:
        with allure.step('fill in the input text of the description'):
            self.fill(self.description_input, text)

    @allure.step('click on the spending creation button')
    def click_on_spending_creation_button(self) -> None:
        self.click(self.create_spend_button)

    @allure.step('click on the drop-down list of spending categories')
    def choose_on_drop_down_list_of_spending_categories(self) -> None:
        self.click(self.category_drop_down_list)

    @allure.step('click on the Input category')
    def click_on_input_category(self) -> None:
        self.click(self.category_input)

    @allure.step('press enter on the keyboard')
    def press_enter_on_keyboard(self) -> None:
        self.press_keyboard(self.spend_date, 'Enter')

    @allure.step('Check that the dropdown is empty')
    def check_that_dropdown_is_empty(self) -> None:
        self.check_element_is_hidden(self.category_drop_down_list)
