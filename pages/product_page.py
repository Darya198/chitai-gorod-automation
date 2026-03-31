import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage


class ProductPage(MainPage):
    def __init__(self, browser) -> None:
        self.browser = browser
        self.buy_button = (By.CSS_SELECTOR,
                           '[data-testid-button-mini-product-card="canBuy"]')
        self.close_catalog_btn = (By.CSS_SELECTOR, ".categories_menu__close")
        self.overlay = (By.CSS_SELECTOR, ".vfm__overlay")
        self.cart_counter = (By.CSS_SELECTOR, 'div.header-controls__indicator')

    @allure.step("Нажать кнопку 'Купить'")
    def add_to_cart(self) -> None:
        wait = WebDriverWait(self.browser, 5)
        try:
            overlay = wait.until(EC.element_to_be_clickable(self.overlay))
            overlay.click()
            print("\n[DEBUG] Оверлей закрыт")
        except Exception:
            print("Ошибка")

        btn = wait.until(EC.element_to_be_clickable(self.buy_button))
        btn.click()
        print("\n[DEBUG] Кнопка 'Купить' нажата успешно!")

    @allure.step("Проверить изменение количества товаров в корзине")
    def get_cart_count(self) -> str:
        wait = WebDriverWait(self.browser, 10)

        counter = wait.until(EC.presence_of_element_located(self.cart_counter))
        return counter.text

    @allure.step("Переход в корзину")
    def go_to_cart(self) -> None:
        wait = WebDriverWait(self.browser, 10)

        cart_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '[aria-label="Корзина"]'))
        )
        cart_btn.click()
        print("\n[DEBUG] Переход в корзину выполнен")

# pytest tests/tests_ui/test_cart_ui.py -s
