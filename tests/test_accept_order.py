import allure

from conftest import new_order_parameters, new_courier_parameters, disposable_courier, disposable_order
from constants import Constants
from routes.courier_routes import CourierRoutes
from routes.order_routes import OrderRoutes


class TestAcceptOrder:
    @allure.title('Принять заказ')
    @allure.description(
        'Создаем заказ, создаем курьера, принимаем заказ, проверяем что заказ принят, удаляем заказ, удаляем курьера')
    def test_accept_order_possible(self, new_order_parameters, new_courier_parameters, disposable_courier):
        orders = OrderRoutes()
        create_order_response = orders.create_order(new_order_parameters)
        get_order_payload = {
            "t": str(create_order_response.json()["track"])
        }
        get_order_response = orders.get_order_by_track(get_order_payload)
        order_id = str(get_order_response.json()["order"]["id"])
        courier_id, new_courier_parameters, response = disposable_courier  # Получаем ID курьера и параметра из фикстуры
        courier_id_payload = {"courierId": str(courier_id)}
        accept_order_response = orders.accept_order(courier_id_payload, order_id)
        assert accept_order_response.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{accept_order_response.status_code}'"
        assert accept_order_response.json()["ok"] == True

    @allure.title('Принять заказ без id курьера')
    @allure.description(
        'Создаем заказ, принимаем заказ без id курьера, проверяем сообщение об ошибке и отменяем заказ')
    def test_accept_order_without_courier_impossible(self, new_order_parameters, disposable_order):
        orders = OrderRoutes()
        order_track, new_order_parameters, response = disposable_order
        get_order_payload = {
            "t": str(response.json()["track"])
        }
        get_order_response = orders.get_order_by_track(get_order_payload)
        order_id = str(get_order_response.json()["order"]["id"])
        courier_id_payload = ''
        accept_order_response = orders.accept_order(courier_id_payload, order_id)
        assert accept_order_response.status_code == 400, f"Ошибка: ожидается статус ответа 400 , но получили '{accept_order_response.status_code}'"
        assert accept_order_response.json()["message"] == Constants.NO_DATA_FOR_SEARCH

    @allure.title('Принять заказ без id заказа')
    @allure.description(
        'Создаем заказ, создаем курьера, принимаем заказ без id заказа, проверяем сообщение об ошибке и отменяем заказ')
    def test_accept_order_without_order_impossible(self, new_order_parameters, new_courier_parameters,
                                                   disposable_courier):
        orders = OrderRoutes()
        order_id = ''
        courier_id, new_courier_parameters, response = disposable_courier  # Получаем ID курьера и параметра из фикстуры
        courier_id_payload = {"courierId": str(courier_id)}
        accept_order_response = orders.accept_order(courier_id_payload, order_id)
        assert accept_order_response.status_code == 404, f"Ошибка: ожидается статус ответа 404 , но получили '{accept_order_response.status_code}'"
        assert accept_order_response.json()["message"] == Constants.NOT_FOUND_MSSG

    @allure.title('Принять заказ с неверным id курьера')
    @allure.description(
        'Создаем заказ, создаем курьера, удаляем курьера, принимаем заказ, проверяем сообщение об ошибке и отменяем заказ')
    def test_accept_order_non_existing_courier_impossible(self, new_order_parameters, new_courier_parameters,
                                                          disposable_courier, disposable_order):
        orders = OrderRoutes()
        order_track, new_order_parameters, response = disposable_order
        get_order_payload = {
            "t": str(response.json()["track"])
        }
        get_order_response = orders.get_order_by_track(get_order_payload)
        order_id = f'{str(get_order_response.json()["order"]["id"])}'
        couriers = CourierRoutes()
        couriers.create_courier(new_courier_parameters)
        courier_id = couriers.login_courier_return_id(new_courier_parameters['login'],
                                                      new_courier_parameters['password'])
        couriers.delete_courier(courier_id)
        courier_id_payload = {"courierId": f'{str(courier_id)}'}
        accept_order_response = orders.accept_order(courier_id_payload, order_id)
        assert accept_order_response.status_code == 404, f"Ошибка: ожидается статус ответа 404 , но получили '{accept_order_response.status_code}'"
        assert accept_order_response.json()["message"] == Constants.COURIER_ID_NOT_EXIST_MSSG

    @allure.title('Принять заказ с неверным id заказа')
    @allure.description(
        'Создаем курьера,  принимаем заказ c несущ айди, проверяем сообщение об ошибке, удаляем курьера')
    def test_accept_order_non_existing_order_impossible(self, new_order_parameters, new_courier_parameters,
                                                        disposable_courier):
        order_id = str(-1)
        courier_id, new_courier_parameters, response = disposable_courier  # Получаем ID курьера и параметра из фикстуры
        courier_id_payload = {"courierId": {str(courier_id)}}
        print('c = ' + str(courier_id) + ' order = ' + order_id)
        accept_order_response = OrderRoutes().accept_order(courier_id_payload, order_id)
        assert accept_order_response.status_code == 404, f"Ошибка: ожидается статус ответа 404 , но получили '{accept_order_response.status_code}'"
        assert accept_order_response.json()["message"] == Constants.ORDER_ID_NOT_EXIST_MSSG
