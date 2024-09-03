from playwright.sync_api import Locator, LocatorAssertions, expect


class MixinSimplifyingLogic:
    """Содержит методы, для упрощения кода."""

    def expect_element(self, locator: Locator | str) -> LocatorAssertions:
        """Вернуть логику ожидания проверки над элементом.

        Выбор логики ожидания происходит вне этого метода, тут лишь LocatorAssertions возвращается.
        """
        if isinstance(locator, Locator):
            return expect(locator)
        return expect(self.driver.locator(locator))

    def get_element(self, locator: Locator | str) -> Locator:
        """Вернуть элемент найденному по локатору."""
        if isinstance(locator, Locator):
            return locator
        return self.driver.locator(locator)
