from playwright.sync_api import Locator, LocatorAssertions, expect


class MixinSimplifyingLogic:
    """Содержит методы, для упрощения кода."""

    def expect_element(self, locator: str) -> LocatorAssertions:
        """Вернуть логику ожидания проверки над элементом.

        Выбор логики ожидания происходит вне этого метода, тут лишь LocatorAssertions возвращается.
        """
        return expect(self.driver.locator(locator))

    def get_element(self, locator: str) -> Locator:
        """Вернуть элемент найденному по локатору."""
        return self.driver.locator(locator)
