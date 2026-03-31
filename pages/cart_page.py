import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from pages.locators import CatalogLocators
from selenium.webdriver.common.keys import Keys
from config import base_url_ui


class CartPage(MainPage):
    url = base_url_ui

    def __init__(self, browser) -> None:
        self.browser = browser
        self.checkout_button = (
            By.XPATH, "//button[contains(., 'Перейти к оформлению')]")
        self.auth_modal_title = (By.XPATH, "//p")

    @allure.step("Нажать кнопку 'Перейти к оформлению'")
    def proceed_to_checkout(self) -> None:
        wait = WebDriverWait(self.browser, 10)
        btn = wait.until(EC.element_to_be_clickable(self.checkout_button))
        btn.click()
        print("\n[DEBUG] Кнопка 'Перейти к оформлению' нажата успешно!")

    @allure.step("Проверить появление окна авторизации")
    def is_auth_modal_visible(self) -> None:
        wait = WebDriverWait(self.browser, 10)
        try:
            wait.until(EC.presence_of_element_located(self.auth_modal_title))
            print("\n[INFO] Необходима авторизация")
            return True
        except Exception:
            current_url = self.browser.current_url
            print(f"\n[INFO] Окно авторизации не появилось. "
                  f"\n[INFO]Текущий URL: {current_url}")
            return False

    @allure.step("Применить несуществующий промокод: {code}")
    def apply_invalid_promo(self, code) -> None:
        input_field = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                CatalogLocators.PROMO_INPUT))
        input_field.send_keys(code)

        input_field.send_keys(Keys.ENTER)

    @allure.step("Получить текст ошибки промокода")
    def get_promo_error_text(self) -> str:
        element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                CatalogLocators.PROMO_ERROR_MESSAGE))
        return element.text

# pytest tests/tests_ui/test_cart_ui.py -s
