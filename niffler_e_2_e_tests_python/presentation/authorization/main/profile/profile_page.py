from niffler_e_2_e_tests_python.base_logic import BaseLogic


class ProfilePage(BaseLogic):
    path = '/profile'

    alert_add_category = "//div[@role='alert']"
    alert_add_category_text = f"{alert_add_category}/div[2]"
    alert_button_close = "//button[@aria-label='close']"
    categories_list = "//ul[@class='categories__list']/li"
    categories_input = "//input[@name='category']"
    categories_button = "//button[@class='button  ' and text()='Create']"
    main_button = "//a[@href='/main']"
    alert_successful_text = 'New category added'
    alert_unsuccessful_text = 'Can not add new category'
    subtitle = '//h2'

    def add_category(self, name_category: str) -> None:
        """Добавляем категорию трат."""
        self.fill(self.categories_input, name_category)
        self.click(self.categories_button)

    def refresh_page_to_update_categories(self, count: int):
        if self.get_element(self.categories_list).count() != count:
            self.refresh_page()
