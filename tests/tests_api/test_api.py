import pytest
import allure
from tests.tests_api.api_client import ChitaiGorodApi
from config import book_id, non_existent_id


@allure.epic("API: Взаимодействие с каталогом и корзиной")
@pytest.mark.api
class TestSearchApi:

    def setup_method(self):
        self.api = ChitaiGorodApi()

    @allure.title("Поиск книг по фразе 'Мастер и Маргарита'")
    def test_search_books(self):
        response = self.api.search_books("Мастер и Маргарита")

        with allure.step("Проверка успешного статус-кода (200 или 204)"):
            assert response.status_code in [200, 204], \
                f"Ожидался успех, но пришел {response.status_code}"

        if response.status_code == 200:
            with allure.step("Проверка содержимого JSON"):
                data = response.json()
                assert "data" in data
                assert len(data["data"]) > 0
        else:
            with allure.step("Сервер вернул 204 (Пустой ответ), "
                             "поиск прошел успешно"):
                print("\n[API INFO]: Поиск выполнен, "
                      "но тело ответа пустое (204)")

    @allure.title("Добавление и последующее удаление товара из корзины")
    def test_add_and_delete_cart(self):
        add_response = self.api.add_to_cart(book_id)
        assert add_response.status_code in [200, 201]

        del_response = self.api.delete_from_cart(book_id)

        with allure.step("Проверка успешного удаления (200 или 204)"):
            assert del_response.status_code in [200, 204], \
                f"Ошибка удаления! Код: {del_response.status_code}"

    @allure.title("Удаление товара из корзины")
    def test_delete_from_cart(self):
        with allure.step("Подготовка: Добавление товара в корзину"):
            add_res = self.api.add_to_cart(book_id)
            assert add_res.status_code in [200, 201], \
                (f"Не удалось добавить товар для теста. "
                 f"Код: {add_res.status_code}")

        import time
        time.sleep(1)

        with allure.step(f"Удаление товара с ID {book_id} из корзины"):
            del_res = self.api.delete_from_cart(book_id)

            assert del_res.status_code in [200, 204], \
                (f"Ошибка при удалении! "
                 f"Сервер вернул код: {del_res.status_code}")

        with allure.step("Вывод результата в консоль"):
            print(f"\n[API LOG]: Товар {book_id} успешно удален. "
                  "fКод: {del_res.status_code}")

    @allure.title("Негативный тест: Запрос несуществующего товара")
    def test_get_non_existent_product(self):
        response = self.api.get_product_info(non_existent_id)

        with allure.step("Проверка, что сервер вернул ошибку (403/404)"):
            assert response.status_code in [403, 404], \
                (f"Ошибка! Ожидался отказ (403/404), "
                 f"но пришел {response.status_code}")

        with allure.step("Проверка текста ошибки"):
            error_text = response.text.lower()
            assert "not found" in error_text or "blocked" in error_text

    @allure.title("Негативный тест: Создание заказа без данных пользователя")
    def test_create_order_without_user_data(self):
        response = self.api.create_order_negative()

        with allure.step("Проверка, что сервер "
                         "отклонил запрос (400, 401, 403 или 422)"):
            assert response.status_code in [400, 401, 403, 422], \
                (f"Ожидалась ошибка валидации, "
                 f"но пришел код {response.status_code}")

        with allure.step("Проверка наличия сообщения"
                         "об ошибке и вывод в консоль"):
            assert len(response.text) > 0
            print(f"\n[API LOG]: Ответ сервера"
                  f"на пустые данные: {response.text}")

# pytest -m api --alluredir=allure-results
