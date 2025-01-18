import allure

from conftest import new_order_parameters, disposable_order
from constants import Constants
from order_routes import OrderRoutes


# Дополнительное задание
class TestGetOrderByTrack:
    @allure.title('Получить заказ по его номеру')
    @allure.description('Создаем заказ, по треку получаем детали заказа, проверяем ответ, закрываем заказ ')
    def test_get_order_by_track(self, new_order_parameters, disposable_order):
        orders = OrderRoutes()
        order_track, new_order_parameters, response = disposable_order

        get_order_payload = {
            "t": str(response.json()["track"])
        }
        response = orders.get_order_by_track(get_order_payload)
        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        for key, value in new_order_parameters.items():
            if key in response.json()["order"] and key != "deliveryDate":
                assert response.json()["order"][
                           key] == value, f"Ключ '{key}', значение '{value}' отсутствует в ответе."
            elif key in response.json()["order"] and key == "deliveryDate":
                assert response.json()["order"][
                           key].split('T')[0] == value, f"Ключ '{key}', значение '{value}' отсутствует в ответе."

    @allure.title('Получить заказ - запрос с несуществующим заказом возвращает ошибку')
    @allure.description('Создаем заказ, отменяем заказ, по треку получаем детали заказа, проверяем ответ, закрываем заказ ')
    def test_get_order_by_not_existing_track_impossible(self, new_order_parameters, disposable_order):
        orders = OrderRoutes()
        response = orders.create_order(new_order_parameters)
        order_track = str(response.json()["track"])
        get_order_payload = {
            "t": order_track
        }
        cancel_order_payload = {
            "track": order_track
        }
        orders.cancel_order(cancel_order_payload)
        response = orders.get_order_by_track(get_order_payload)
        assert response.status_code == 404 , f"Ошибка: ожидается статус ответа 404 , но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.ORDER_NOT_FOUND_MSSG


    @allure.title('Получить заказ - запрос без номера заказа возвращает ошибку')
    @allure.description('По треку получаем детали заказа без его номера, проверяем ответ')
    def test_get_order_without_track_impossible(self, new_order_parameters, disposable_order):
        get_order_payload = {
            "t": ""
        }
        response = OrderRoutes().get_order_by_track(get_order_payload)
        assert response.status_code == 400 , f"Ошибка: ожидается статус ответа 400, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.NO_DATA_FOR_SEARCH
