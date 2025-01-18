import random

import pytest

from helpers import RandomHelper


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
def updated_courier_parameters(parameters):
    parameters_updated = parameters
    parameters_updated["password"] = f"{parameters["password"]}_updated"
    parameters_updated["firstName"] = f"{parameters["firstName"]}_updated"
    return parameters_updated
