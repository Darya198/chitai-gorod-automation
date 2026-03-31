import requests
import allure
from config import base_url_api, token_value
from config import order_address, user_id, shipment_id, point_id


class ChitaiGorodApi:
    def __init__(self):
        self.base_url = base_url_api
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Authorization": token_value,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        })

    @allure.step("API: Поиск товара по фразе: {search_phrase}")
    def search_books(self, search_phrase: str, result_count: int = 15):
        url = f"{self.base_url}/web/api/v2/search/results"
        payload = {
            "searchPhrase": search_phrase,
            "resultCount": result_count
        }
        return self.session.post(url, json=payload)

    @allure.step("API: Добавление товара в корзину по ID: {item_id}")
    def add_to_cart(self, item_id: int):
        url = f"{self.base_url}/web/api/v1/cart/product"
        payload = {"id": item_id}
        return self.session.post(url, json=payload)

    @allure.step("API: Удаление товара из корзины по ID: {item_id}")
    def delete_from_cart(self, item_id: int):
        url = f"{self.base_url}/web/api/v1/cart/product"
        payload = {"id": item_id}
        return self.session.post(url, json=payload)

    @allure.step("API: Получение информации о товаре по ID: {product_id}")
    def get_product_info(self, product_id: int):
        url = f"{self.base_url}/web/api/v1/products/other-edits/{product_id}"
        return self.session.get(url)

    @allure.step("API: Попытка создания заказа с пустыми данными пользователя")
    def create_order_negative(self):
        url = f"{self.base_url}/web/api/v2/orders"
        payload = {
            "address": order_address,
            "shipment": {"id": shipment_id,
                         "pointId": point_id, "type": "shop"},
            "user": {
                "email": "", "name": "", "phone": "",
                "type": "individual",
                "userId": user_id
            }
        }

        headers = {"X-App-Id": "v2"}
        return self.session.post(url, json=payload, headers=headers)
