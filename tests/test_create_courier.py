import allure
import pytest
from conftest import new_courier_parameters, updated_courier_parameters
from constants import Constants
from courier_routes import CourierRoutes


class TestCreateCourier:
    @allure.title('Курьера можно создать')
    @allure.description('Создаем курьера, проверяем создание курьера, логинимся под ним, удаляем курьера')
    def test_create_courier_possible(self, new_courier_parameters):
        courier = CourierRoutes()
        response = courier.create_courier(new_courier_parameters)
        assert response.status_code == 201, f"Ошибка: ожидается статус ответа 201, но получили '{response.status_code}'"
        assert response.json()['ok'] == True
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        courier.delete_courier(courier_id)

    @allure.title('Нельзя создать двух одинаковых курьеров')
    @allure.description(
        'Создаем курьера, создаем курьера с аналогичными параметрами, проверяем сообщение об ошибке, логинимся под курьером, удаляем курьера')
    def test_create_existing_courier_impossible(self, new_courier_parameters):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        response = courier.create_courier(new_courier_parameters)
        assert response.status_code == 409, f"Ошибка: ожидается статус ответа 409, но получили '{response.status_code}'"
        assert response.json()['message'] == Constants.CREATE_COURIER_LOGIN_USED_MSSG
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        courier.delete_courier(courier_id)

    @allure.title('Нельзя создать курьера без параметров')
    @allure.description('Создаем курьера и не указываем параметры, проверяем сообщение об ошибке')
    @pytest.mark.parametrize("missing_key", ["login", "password", "firstName"])
    def test_create_existing_courier_impossible(self, courier_parameters, missing_key):
        courier = CourierRoutes()
        courier_parameters_missed_key = {k: v for k, v in courier_parameters.items() if k != missing_key}
        response = courier.create_courier(courier_parameters_missed_key)
        assert response.status_code == 400, f"Ошибка: ожидается статус ответа 400, но получили '{response.status_code}'"
        assert response.json()['message'] == Constants.CREATE_COURIER_NO_DATA_MSSG

    @allure.title('Нельзя создать курьера с логином, который уже есть')
    @allure.description(
        'Создаем курьера, создаем курьера с уже существующим логином, проверяем сообщение об ошибке, логинимся под курьером, удаляем курьера')
    def test_create_existing_courier_impossible(self, new_courier_parameters, updated_courier_parameters):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        response = courier.create_courier(updated_courier_parameters)
        assert response.status_code == 409, f"Ошибка: ожидается статус ответа 409, но получили '{response.status_code}'"
        assert response.json()['message'] == Constants.CREATE_COURIER_LOGIN_USED_MSSG
        courier.delete_courier(courier_id)
