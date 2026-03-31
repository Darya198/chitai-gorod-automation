import allure
import pytest
from pages.main_page import MainPage
from pages.product_page import ProductPage
import time
from pages.cart_page import CartPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.locators import CatalogLocators
from config import invalid_promo, product_url


@pytest.mark.ui
@allure.epic("Корзина")
@allure.feature("Добавление товара")
class TestCartUI:

    @allure.story("Добавление книги в корзину из карточки товара")
    @allure.title("Успешное добавление товара и переход к оформлению")
    def test_add_book_to_cart(self, auth_browser):
        main_page = MainPage(auth_browser)
        product_page = ProductPage(auth_browser)
        cart_page = CartPage(auth_browser)

        main_page.open()
        main_page.clean_ui()
        main_page.search("Мастер и Маргарита")
        main_page.click_first_product()

        product_page.add_to_cart()
        product_page.get_cart_count()

        with allure.step("Переход в корзину"):
            product_page.go_to_cart()
            time.sleep(3)

        cart_page.proceed_to_checkout()
        time.sleep(5)
        with allure.step("Проверка окна авторизации"):
            is_visible = cart_page.is_auth_modal_visible()
            assert is_visible is True, "Ошибка!"
            " Не удалось добраться до этапа оформления"


@pytest.mark.ui
@allure.epic("Корзина")
@allure.feature("Промокоды")
class TestCartPromoUI:

    @allure.story("Проверка работы поля промокода при вводе невалидных данных")
    @allure.title("Негативный сценарий: ввод неверного промокода")
    def test_invalid_promo_code(self, browser):
        page = ProductPage(browser)
        page.open(product_url)
        page.clean_ui()

        wait = WebDriverWait(browser, 10)
        btn = wait.until(
            EC.element_to_be_clickable(CatalogLocators.buy_button))
        btn.click()
        print("\n[DEBUG] Кнопка 'Купить' нажата успешно!")
        page.get_cart_count()
        page.go_to_cart()

        cart_page = CartPage(browser)
        cart_page.apply_invalid_promo(invalid_promo)

        error_text = cart_page.get_promo_error_text()
        print(f"\n[PROMO ERROR]: {error_text}")

        assert "не существует" in error_text.lower(
        ) or "не найден" in error_text.lower(), \
            f"Ожидали сообщение об ошибке промокода, но получили: {error_text}"

# pytest tests/tests_ui/test_cart_ui.py -s
