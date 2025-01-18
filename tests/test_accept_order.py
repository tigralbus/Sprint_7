import allure

from conftest import new_order_parameters, new_courier_parameters
from courier_routes import CourierRoutes
from order_routes import OrderRoutes


class TestAcceptOrder:
    @allure.title('Принять заказ')
    @allure.description(
        'Создаем заказ, создаем курьера, принимаем заказ, проверяем что заказ принят, удаляем заказ, удаляем курьера')
    def test_create_order_parametrized(self, new_order_parameters, new_courier_parameters):
        order = OrderRoutes()
        create_order_response = order.create_order(new_order_parameters)
        get_order_payload = {
            "t": str(create_order_response.json()["track"])
        }
        get_order_response = order.get_order_by_track(get_order_payload)
        order_id = str(get_order_response.json()["order"]["id"])
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        courier_id_payload = {"courierId": str(courier_id)}
        accept_order_response = order.accept_order(courier_id_payload, order_id)
        assert accept_order_response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{accept_order_response.status_code}'"
        assert accept_order_response.json()["ok"] == True

        courier.delete_courier(courier_id)
