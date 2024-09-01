from typing import TYPE_CHECKING, Optional

import allure

from niffler_e_2_e_tests_python.helper_logic import MixinSimplifyingLogic

if TYPE_CHECKING:
    from playwright.sync_api import Page


class BaseSimplifyingLogic(MixinSimplifyingLogic):
    """Содержит в себе методы, для работы с UI."""

    def __init__(self, driver: 'Page'):
        self.driver = driver

    @allure.step('Нажать на элемент по этому локатору: {locator}')
    def click(self, locator: str) -> None:
        """Нажать на элемент страницы."""
        self.get_element(locator).click()

    @allure.step(
        'Нажать у элемента по этому локатору: \'{locator}\' клавишу на клавиатуре: \'{key}\'',
    )
    def press_keyboard(self, locator: str, key: str) -> None:
        """Нажать кнопку на клавиатуре."""
        self.get_element(locator).press(key)

    @allure.step(
        'Заполнить поле элемента по этому локатору: \'{locator}\' текстом: \'{value}\'',
    )
    def fill(self, locator: str, value: str) -> None:
        """Ввести данные в Input на странице."""
        self.get_element(locator).fill(value)

    @allure.step('Открыть страницу по этому Url: \'{url}\'')
    def goto_url(self, url: str) -> None:
        """Переходим по url."""
        self.driver.goto(url)

    @allure.step(
        'Проверить у элемента по этому локатору: \'{locator}\' наличие текста: \'{text}\'',
    )
    def check_text_in_element(self, locator: str, text: str) -> None:
        """Проверить ожидаемый текст в элементе."""
        self.expect_element(locator).to_have_text(text)

    @allure.step(
        'Получить у элемента по этому локатору: \'{locator}\' текст и вернуть текст разделив его'
        'по split: {split}',
    )
    def get_text_in_elements(self, locator: str, split: Optional[str] = None) -> list[str] | list:
        """Получить текст из элементов.

        Если разделять "split" нечего, то отдаем все элементы как они есть.
        """
        if split:
            return self.get_element(locator).all_inner_texts()[0].split(split)
        else:
            return self.get_element(locator).all_inner_texts()

    @allure.step(
        'Проверить у элемента по этому локатору: \'{locator}\' ожидаемое количество элементов: '
        '{quantity}',
    )
    def expected_number_of_items(self, locator: str, quantity: int) -> None:
        """Проверить ожидаемое количество элементов."""
        self.expect_element(locator).to_have_count(quantity)

    @allure.step(
        'Проверить у элемента по этому локатору: \'{locator}\' что он видим и находится в DOM',
    )
    def check_element_is_visible(self, locator: str) -> None:
        """Проверить, видим ли элемент, иначе ошибку выдаем.

        https://playwright.dev/python/docs/actionability#visible
        """
        self.expect_element(locator).to_be_visible()

    @allure.step(
        'Проверить у элемента по этому локатору: \'{locator}\' что он невидим и не находится в DOM',
    )
    def check_element_is_hidden(self, locator: str) -> None:
        """Проверить, невидим ли элемент, иначе ошибку выдаем.

        https://playwright.dev/python/docs/actionability#visible
        """
        self.expect_element(locator).to_be_hidden()

    @allure.step('Обновить страницу')
    def refresh_page(self) -> None:
        """Обновить страницу."""
        self.driver.reload()
