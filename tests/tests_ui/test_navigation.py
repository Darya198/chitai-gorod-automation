from pages.catalog_page import CatalogPage
import pytest
import allure


@pytest.mark.ui
@allure.epic("Навигация по сайту")
@allure.feature("Каталог и хлебные крошки")
@allure.story("Полный цикл перехода по категориям и возврат на главную")
def test_full_catalog_navigation_cycle(browser):
    page = CatalogPage(browser)
    page.open()
    page.clean_ui()
    page.go_to_category()
    page.go_back_to_books_via_breadcrumbs()
    page.return_to_home_via_logo()

# pytest tests/tests_ui/test_navigation.py -s
