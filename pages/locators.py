from selenium.webdriver.common.by import By


class CatalogLocators:
    CATALOG_BTN = (By.CSS_SELECTOR, ".catalog-btn")
    ROOT_CATEGORY = (
        By.XPATH, "(//div[@class='categories-level-menu']//span)[5]")
    SUBROOT_CATEGORY = (
        By.XPATH, "//div[contains(@class, 'categories-level-menu')]"
        "//a[contains(@class, 'categories-level-menu__item')]")
    BREADCRUMBS_STEP_BACK = (
        By.XPATH, "//div[contains(@class, 'breadcrumbs')]//a")
    MAIN_LOGO = (By.CSS_SELECTOR, ".header-sticky__logo-link")
    EMPTY_RESULT_MESSAGE = (By.CSS_SELECTOR, ".catalog-stub__title")
    PROMO_INPUT = (By.CSS_SELECTOR, "input[placeholder='Промокод']")
    PROMO_ERROR_MESSAGE = (By.CSS_SELECTOR, ".promo-code__message")
    buy_button = (
        By.CSS_SELECTOR, '[data-testid-button-mini-product-card="canBuy"]')


# pytest tests/tests_ui/test_navigation.py -s
