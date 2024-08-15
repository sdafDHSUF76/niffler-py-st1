from typing import TYPE_CHECKING

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
