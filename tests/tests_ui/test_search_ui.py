import pytest
import allure
from pages.main_page import MainPage
from config import search_query, invalid_search_query


@pytest.mark.ui
@allure.epic("UI тесты Читай-город")
@allure.feature("Поиск товаров")
class TestSearchUI:

    @allure.story("Поиск конкретной книги и просмотр её данных")
    @allure.title("Поиск книги 'Мастер и Маргарита' и переход в карточку")
    def test_search_and_open_product(self, auth_browser):
        main_page = MainPage(auth_browser)

        main_page.open()
        main_page.clean_ui()
        main_page.search(search_query)
        main_page.click_first_product()

        with allure.step("Проверка: открыта страница товара"):
            assert "product/" in auth_browser.current_url, (
                f"Ошибка! Ожидали карточку товара, "
                f"но открыт URL: {auth_browser.current_url}")

    @allure.story("Обработка ситуации, когда товар не найден")
    @allure.title("Негативный поиск: проверка сообщения 'Ничего не найдено'")
    def test_search_invalid_product(self, auth_browser):
        main_page = MainPage(auth_browser)
        main_page.open()
        main_page.clean_ui()

        main_page.search(invalid_search_query)

        with allure.step("Получение текста ошибки с экрана и вывод в консоль"):
            error_text = main_page.get_empty_result_message()
            print(f"\n[РЕЗУЛЬТАТ ПОИСКА]: {error_text}")

            assert "Похоже, у нас такого нет" in error_text, \
                f"Ожидали текст об ошибке, но получили: {error_text}"

# pytest tests/tests_ui/test_search_ui.py -s
