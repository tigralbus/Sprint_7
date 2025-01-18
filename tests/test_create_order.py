import allure
import pytest

from conftest import new_order_parameters, disposable_order_with_color


class TestCreateOrder:
    @allure.title('Заказ можно создать c разными значениями цвета самоката')
    @allure.description('Создаем заказ, проверяем создание заказа, отменяем заказ')
    @pytest.mark.parametrize('color', [["BLACK", "GRAY"], ["BLACK", ""], ["", "GRAY"], []])
    def test_create_order_parametrized(self, new_order_parameters, color, disposable_order_with_color):
        order_parameters, response = disposable_order_with_color
        assert response.status_code == 201, f"Ошибка: ожидается статус ответа 201, но получили '{response.status_code}'"
        assert response.json()["track"]
