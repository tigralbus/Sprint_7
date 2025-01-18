import json
import random
import pytest

from courier_routes import CourierRoutes
from helpers import RandomHelper
from order_routes import OrderRoutes


@pytest.fixture(scope='function')
def disposable_courier(new_courier_parameters):
    couriers = CourierRoutes()
    # Создаем курьера и получаем его ID
    response = couriers.create_courier(new_courier_parameters)
    courier_id = couriers.login_courier_return_id(new_courier_parameters['login'], new_courier_parameters['password'])
    yield courier_id, new_courier_parameters, response  # Передаем ID курьера в тест
    # Выполняем удаление курьера после завершения теста
    couriers.delete_courier(courier_id)


@pytest.fixture(scope='function')
def disposable_order_with_color(new_order_parameters, color):
    orders = OrderRoutes()
    new_order_parameters["color"] = color
    create_order_payload = json.dumps(new_order_parameters)
    response = orders.create_order(create_order_payload)
    cancel_order_payload = {
        "track": str(response.json()["track"])
    }
    yield new_order_parameters, response
    orders.cancel_order(cancel_order_payload)


@pytest.fixture(scope='function')
def disposable_order(new_order_parameters):
    orders = OrderRoutes()
    response = orders.create_order(new_order_parameters)
    order_track = str(response.json()["track"])
    cancel_order_payload = {
        "track": order_track
    }
    yield order_track, new_order_parameters, response
    orders.cancel_order(cancel_order_payload)


@pytest.fixture(scope='function')
def new_courier_parameters():
    # генерируем логин, пароль и имя курьера
    login = RandomHelper.random_string(10)
    password = RandomHelper.random_string(10)
    first_name = RandomHelper.random_string(10)

    # собираем тело запроса
    parameters = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return parameters


@pytest.fixture(scope='function')
def new_order_parameters():
    # генерируем параметры для заказа
    first_mame = RandomHelper.random_string(10)
    last_name = RandomHelper.random_string(10)
    address = f"город Москва, улица {RandomHelper.random_string(10)}, дом 13"
    metro_station = str(random.randint(1, 25))
    phone = f"+7{random.randint(1111111111, 9999999999)}"
    rent_time = random.randint(1, 5)
    delivery_date = "2023-12-31"
    comment = RandomHelper.random_string(10)
    color = ["BLACK", "GRAY"]
    # собираем тело запроса
    parameters = {
        "firstName": first_mame,
        "lastName": last_name,
        "address": address,
        "metroStation": metro_station,
        "phone": phone,
        "rentTime": rent_time,
        "deliveryDate": delivery_date,
        "comment": comment,
        "color": color
    }
    return parameters


@pytest.fixture(scope='function')
def orders_list_parameters():
    nearest_station = [str(random.randint(1, 25))]
    parameters = {
        # 'nearestStation': '["13"]', 'limit': 3, 'page': 0
        'nearestStation': f'["{nearest_station}"]', 'limit': 3, 'page': 0
    }
    return parameters


@pytest.fixture(scope='function')
def updated_courier_parameters(new_courier_parameters):
    parameters_updated = new_courier_parameters
    parameters_updated["password"] = f"{new_courier_parameters["password"]}_updated"
    parameters_updated["firstName"] = f"{new_courier_parameters["firstName"]}_updated"
    return parameters_updated
