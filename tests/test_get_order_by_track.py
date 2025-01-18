import allure

from conftest import new_order_parameters
from order_routes import OrderRoutes


# Дополнительное задание
class TestGetOrderByTrack:
    @allure.title('Получить заказ по его номеру')
    @allure.description('Создаем заказ, по треку получаем детали заказа, проверяем ответ, закрываем заказ ')
    def test_get_order_by_track(self, new_order_parameters):
        order = OrderRoutes()
        create_response = order.create_order(new_order_parameters)
        get_order_payload = {
            "t": str(create_response.json()["track"])
        }
        response = order.get_order_by_track(get_order_payload)
        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        for key, value in new_order_parameters.items():
            if key in response.json()["order"] and key != "deliveryDate":
                assert response.json()["order"][
                           key] == value, f"Ключ '{key}', значение '{value}' отсутствует в ответе."

        cancel_order_payload = {
            "track": str(create_response.json()["track"])
        }
        order.cancel_order(cancel_order_payload)
