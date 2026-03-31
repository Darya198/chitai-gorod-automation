import allure
from pages.main_page import MainPage
from pages.locators import CatalogLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CatalogPage(MainPage):
    @allure.step("Переход в категорию и подкатегорию каталога")
    def go_to_category(self) -> None:
        self.browser.find_element(
            CatalogLocators.CATALOG_BTN[0],
            CatalogLocators.CATALOG_BTN[1]).click()

        root_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(CatalogLocators.ROOT_CATEGORY))
        root_btn.click()

        subroot_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(CatalogLocators.SUBROOT_CATEGORY))
        subroot_btn.click()

    @allure.step("Возврат в предыдущий раздел через хлебные крошки")
    def go_back_to_books_via_breadcrumbs(self) -> None:
        self.browser.find_element(
            CatalogLocators.BREADCRUMBS_STEP_BACK[0],
            CatalogLocators.BREADCRUMBS_STEP_BACK[1]).click()

    @allure.step("Возврат на главную страницу через клик по логотипу")
    def return_to_home_via_logo(self) -> None:
        self.browser.find_element(
            CatalogLocators.MAIN_LOGO[0],
            CatalogLocators.MAIN_LOGO[1]).click()

# pytest tests/tests_ui/test_navigation.py -s
