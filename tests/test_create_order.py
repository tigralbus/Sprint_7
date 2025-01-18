import json
import allure
import pytest

from conftest import new_order_parameters
from order_routes import OrderRoutes


class TestCreateOrder:
    @allure.title('Заказ можно создать')
    @allure.description('Создаем заказ, проверяем создание заказа, отменяем заказ')
    @pytest.mark.parametrize('color', [["BLACK", "GRAY"], ["BLACK", ""], ["", "GRAY"], []])
    def test_create_order_parametrized(self, new_order_parameters, color):
        new_order_parameters["color"] = color
        create_order_payload = json.dumps(new_order_parameters)
        order = OrderRoutes()
        response = order.create_order(create_order_payload)
        print(response.status_code)
        r = response.json()
        print(r)
        print(new_order_parameters)
        assert response.status_code == 201, f"Ошибка: ожидается статус ответа 201, но получили '{response.status_code}'"
        assert response.json()["track"]
        cancel_order_payload = {
            "track": str(response.json()["track"])
        }
        order.cancel_order(cancel_order_payload)
