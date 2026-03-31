import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from config import base_url_ui, token_value


@pytest.fixture
def browser():
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def auth_browser(browser):
    browser.get(base_url_ui)
    browser.add_cookie({"name": "access-token", "value": token_value})
    browser.refresh()
    yield browser
