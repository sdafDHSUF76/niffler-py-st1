from typing import TYPE_CHECKING, Optional

from playwright.sync_api import expect

if TYPE_CHECKING:
    from playwright.sync_api import Page


class BaseLogic:

    def __init__(self, driver: 'Page'):
        self.driver = driver

    def click(self, locator: str) -> None:
        """Нажать на элемент страницы."""
        self.driver.locator(locator).click()

    def fill(self, locator: str, value: str) -> None:
        """Ввести данные в Input на странице."""
        self.driver.locator(locator).fill(value)

    def goto_url(self, url: str) -> None:
        """Переходим по url."""
        self.driver.goto(url)

    def check_text_in_element(self, locator: str, text: str) -> None:
        """Проверить ожидаемый текст в элементе."""
        expect(self.driver.locator(locator)).to_have_text(text)

    def get_text_in_elements(self, locator: str, split: Optional[str] = None) -> list[str] | list:
        """Получить текст из элементов.

        Если разделять "split" нечего, то отдаем все элементы как они есть.
        """
        if split:
            return self.driver.locator(locator).all_inner_texts()[0].split(split)
        else:
            return self.driver.locator(locator).all_inner_texts()

    def expected_number_of_items(self, locator: str, quantity: int) -> None:
        """Проверить ожидаемое количество элементов."""
        expect(self.driver.locator(locator)).to_have_count(quantity)
