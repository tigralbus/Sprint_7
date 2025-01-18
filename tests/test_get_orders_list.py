import allure

from conftest import orders_list_parameters
from constants import Constants
from order_routes import OrderRoutes

# Дополнительное задание
class TestGetOrdersList:
    @allure.title('Получить список заказов')
    @allure.description('Получаем список заказов, проверяем его структуру и количество записей')
    def test_get_order_list_returned_data_updated(self, orders_list_parameters):
        orders = OrderRoutes()
        response = orders.get_orders_list(orders_list_parameters)
        assert response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert isinstance(response.json()["orders"], list)
        for item in Constants.ORDER_RESPONSE_KEYS:
            for index in range(len(response.json()["orders"])):
                assert item in response.json()["orders"][index]
