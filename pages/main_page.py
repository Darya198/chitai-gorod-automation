import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.locators import CatalogLocators
from config import base_url_ui


class MainPage:
    def __init__(self, browser):
        self.browser = browser
        self.url = base_url_ui

        self.search_input = (By.ID, "app-search")
        self.first_product_card = (By.CSS_SELECTOR, ".product-card__content")
        self.search_button = (By.CSS_SELECTOR, "button[aria-label='Найти']")
        self.product_card = (By.CSS_SELECTOR, ".product_card")

    @allure.step("Открыть главную страницу")
    def open(self, url=None) -> None:
        target_url = url if url else self.url
        self.browser.get(target_url)

        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        return self

    @allure.step("Закрытие баннеров (двойная проверка)")
    def clean_ui(self) -> None:
        targets = [
            (By.CSS_SELECTOR, "div.popmechanic-close"),
            (By.CSS_SELECTOR, "button.agreement-notice__button"),
            (By.CSS_SELECTOR,
             "button.chg-app-button--primary.chg-app-button--block")
        ]

        for attempt in range(2):
            for locator in targets:
                try:
                    element = WebDriverWait(self.browser, 3).until(
                        EC.element_to_be_clickable(locator))
                    element.click()
                    print(f"Окно {locator} закрыто с {attempt + 1} раза")
                except Exception:
                    print("Окно подписки не найдено")
        return self

    @allure.step("Поиск товара по названию: {text}")
    def search(self, text: str) -> None:
        wait = WebDriverWait(self.browser, 2)

        search_field = wait.until(
            EC.element_to_be_clickable(self.search_input))
        search_field.click()
        search_field.clear()
        search_field.send_keys(text)

        search_field.send_keys(Keys.ESCAPE)

        btn = wait.until(EC.element_to_be_clickable(self.search_button))
        btn.click()

    @allure.step("Кликнуть по первому товару в результатах поиска")
    def click_first_product(self) -> None:
        wait = WebDriverWait(self.browser, 20)

        background = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, ".global-white-backing")))
        background.click()

        first_card = wait.until(
            EC.element_to_be_clickable(self.first_product_card))
        first_card.click()

        wait.until(EC.url_contains("product/"))
        print("Переход в карточку товара выполнен успешно!")

    @allure.step("Поиск несуществующего товара")
    def get_empty_result_message(self) -> str:
        message_element = WebDriverWait(
            self.browser, 10).until(
                EC.visibility_of_element_located(
                    CatalogLocators.EMPTY_RESULT_MESSAGE))
        return message_element.text
