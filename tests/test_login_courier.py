import allure
import pytest

from conftest import new_courier_parameters
from constants import Constants
from courier_routes import CourierRoutes


class TestLoginCourier:
    @allure.title('Курьер может залогиниться')
    @allure.description('Создаем курьера, логинимся под ним, проверяем логин, удаляем курьера')
    def test_login_courier_possible(self, new_courier_parameters):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        response_login = courier.login_courier(new_courier_parameters['login'], new_courier_parameters['password'])
        assert response_login.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response_login.status_code}'"
        assert response_login.json()["id"]

    @allure.title('Для авторизации курьера нужно передать все обязательные поля')
    @allure.description(
        'Создаем курьера, логинимся под ним без пароля/логина, проверяем ошибку, удаляем курьера')
    @pytest.mark.parametrize("missing_key", ["login", "password"])
    def test_login_courier_critical_fields_required(self, new_courier_parameters, missing_key):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        new_courier_parameters_miss_key = new_courier_parameters.copy()
        new_courier_parameters_miss_key[missing_key] = ''
        response = courier.login_courier(new_courier_parameters_miss_key.get("login"),
                                         new_courier_parameters_miss_key.get("password"))
        assert response.status_code == 400, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.NO_DATA_FOR_LOGIN_MSSG
        courier.delete_courier(courier_id)

    @allure.title('Cистема вернёт ошибку, если неправильно указать логин или пароль')
    @allure.description(
        'Создаем курьера, логинимся под ним под неправильными паролем/логином, проверяем ошибку, удаляем курьера')
    @pytest.mark.parametrize("wrong_key", ["login", "password"])
    def test_login_courier_incorrect_parameters(self, new_courier_parameters, wrong_key):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        new_courier_parameters_wrong_key = new_courier_parameters.copy()
        new_courier_parameters_wrong_key[wrong_key] = 'wrong_value'
        response = courier.login_courier(new_courier_parameters_wrong_key.get("login"),
                                         new_courier_parameters_wrong_key.get("password"))
        assert response.status_code == 404, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.ACCOUNT_NOT_FOUND_MSSG
        courier.delete_courier(courier_id)

    @allure.title('Cистема вернёт ошибку, если неправильно указать логин или пароль')
    @allure.description(
        'Создаем курьера, логинимся под ним под неправильными паролем/логином, проверяем ошибку, удаляем курьера')
    def test_login_courier_incorrect_parameters(self, new_courier_parameters):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        courier.delete_courier(courier_id)
        response = courier.login_courier(new_courier_parameters['login'],
                                         new_courier_parameters['password'])
        assert response.status_code == 404, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.ACCOUNT_NOT_FOUND_MSSG
