from typing import TYPE_CHECKING

import allure

from niffler_e_2_e_tests_python.base_logic import BaseLogic

if TYPE_CHECKING:
    from playwright.sync_api import Page

class MainPage(BaseLogic):
    path = '/main'

    def __init__(self, driver: 'Page'):
        super().__init__(driver)
        self.header = self.driver.locator('//h1')
        self.logout_button = self.driver.locator(
            "//button[contains(@class,'button-icon_type_logout')]"
        )
        self.profile_button = self.driver.locator("//a[@href='/profile']")
        self.main = self.driver.locator("//a[@href='/main']")
        self.category_input = self.driver.locator(
            "//form[@class='add-spending__form']//div[@class=' css-1dx5uak']"
        )
        self.category_drop_down_list = self.driver.locator("//div[@role='option']")
        self.input_number = self.driver.locator("//input[@type='number']")
        self.spend_date = self.driver.locator(
            "//div[contains(@class,'datepicker')]/input[@type='text']"
        )
        self.description_input = self.driver.locator(
            "//input[@class='form__input ' and @type='text']"
        )
        self.create_spend_button = self.driver.locator("//button[@type='submit']")
        self.spends = self.driver.locator("//tbody/tr")
        self.spend_amount = self.driver.locator('//tbody/tr/td[3]//span')
        self.checkbox_choose_spend = self.driver.locator("//td/input[@type='checkbox']")
        self.button_delete = self.driver.locator(
            "//section[@class='spendings__bulk-actions']/button"
        )

    text_header = 'Niffler. The coin keeper.'

    @allure.step('log out of your account')
    def click_logout(self):
        """Выход из аккаунта через UI."""
        self.click(self.logout_button)

    @allure.step('click on the profile button')
    def click_profile_button(self):
        """Нажать на кнопку Профиля."""
        self.click(self.profile_button)

    @allure.step('click on the main button')
    def click_main_button(self):
        """Нажать на кнопку Профиля."""
        self.click(self.main)

    def check_number_of_expenses_in_spending_history(self, expected_quantity: int) -> None:
        """Проверить количество трат в истории трат."""
        with allure.step('check the number of entries in your spending history'):
            self.expected_number_of_items(self.spends, expected_quantity)

    @allure.step('click on the checkbox next to the spending record')
    def click_on_checkbox_at_selected_expense(self) -> None:
        """Нажать на чекбокс у траты."""
        self.click(self.checkbox_choose_spend)

    @allure.step('click on the delete selected expenses button')
    def click_on_delete_spending_button(self) -> None:
        """Нажать на кнопку удаления выбранных трат."""
        self.click(self.button_delete)

    def fill_input_category(self, text: str) -> None:
        """Вводим данные в input категории трат."""
        with allure.step('fill in the input text of the category'):
            self.fill(self.category_input, text)

    def fill_input_amount_of_spending(self, text: str) -> None:
        """Вводим данные в input количество трат."""
        with allure.step('fill in the input text of the amount of spending'):
            self.fill(self.input_number, text)

    def fill_input_spend_date(self, text: str) -> None:
        """Вводим данные в input дату трат."""
        with allure.step('fill in the input text of the spend date'):
            self.fill(self.spend_date, text)

    def fill_input_description(self, text: str) -> None:
        """Вводим данные в input description."""
        with allure.step('fill in the input text of the description'):
            self.fill(self.description_input, text)

    @allure.step('click on the spending creation button')
    def click_on_spending_creation_button(self) -> None:
        """Нажать на кнопку создания трат."""
        self.click(self.create_spend_button)

    @allure.step('click on the drop-down list of spending categories')
    def choose_on_drop_down_list_of_spending_categories(self) -> None:
        """Выбрать из выпадающего списка категорию трат."""
        self.click(self.category_drop_down_list)

    @allure.step('click on the Input category')
    def click_on_input_category(self) -> None:
        """Нажать на input категорий трат."""
        self.click(self.category_input)

    @allure.step('press enter on the keyboard')
    def press_enter_on_keyboard(self) -> None:
        """Нажать на клавишу Enter На клавиатуре."""
        self.press_keyboard(self.spend_date, 'Enter')

    @allure.step('Check that the dropdown is empty')
    def check_that_dropdown_is_empty(self) -> None:
        """Проверить текст подсказки."""
        self.check_element_is_hidden(self.category_drop_down_list)
