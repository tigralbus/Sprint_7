import allure
import pytest

from conftest import new_courier_parameters, disposable_courier
from constants import Constants
from courier_routes import CourierRoutes


class TestLoginCourier:
    @allure.title('Курьер может залогиниться')
    @allure.description('Создаем курьера, логинимся под ним, проверяем логин, удаляем курьера')
    def test_login_courier_possible(self, new_courier_parameters, disposable_courier):
        couriers = CourierRoutes()
        courier_id, new_courier_parameters, response = disposable_courier  # Получаем ID курьера и параметра из фикстуры
        response_login = couriers.login_courier(new_courier_parameters['login'], new_courier_parameters['password'])
        assert response_login.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response_login.status_code}'"
        assert response_login.json()["id"]

    @allure.title('Для авторизации курьера нужно передать все обязательные поля')
    @allure.description(
        'Создаем курьера, логинимся под ним без пароля/логина, проверяем ошибку, удаляем курьера')
    @pytest.mark.parametrize("missing_key", ["login", "password"])
    def test_login_courier_critical_fields_required(self, new_courier_parameters, missing_key, disposable_courier):
        couriers = CourierRoutes()
        courier_id, new_courier_parameters, response = disposable_courier  # Получаем ID курьера и параметра из фикстуры
        # Изменяем параметры для теста
        new_courier_parameters_miss_key = new_courier_parameters.copy()
        new_courier_parameters_miss_key[missing_key] = ''
        response = couriers.login_courier(new_courier_parameters_miss_key.get("login"),
                                         new_courier_parameters_miss_key.get("password"))
        assert response.status_code == 400, f"Ошибка: ожидается статус ответа 200, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.NO_DATA_FOR_LOGIN_MSSG

    @allure.title('Cистема вернёт ошибку, если неправильно указать логин или пароль') #updated
    @allure.description(
        'Создаем курьера, логинимся под ним под неправильными паролем/логином, проверяем ошибку, удаляем курьера')
    @pytest.mark.parametrize("wrong_key", ["login", "password"])
    def test_login_courier_incorrect_parameters(self, wrong_key, new_courier_parameters, disposable_courier):
        couriers = CourierRoutes()
        courier_id, new_courier_parameters, response = disposable_courier  # Получаем ID курьера и параметра из фикстуры
        # Изменяем параметры для теста
        new_courier_parameters_wrong_key = new_courier_parameters.copy()
        new_courier_parameters_wrong_key[wrong_key] = 'wrong_value'
        # Логинимся с неправильными параметрами
        response = couriers.login_courier(new_courier_parameters_wrong_key.get("login"),
                                          new_courier_parameters_wrong_key.get("password"))
        assert response.status_code == 404, f"Ошибка: ожидается статус ответа 404, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.ACCOUNT_NOT_FOUND_MSSG

    @allure.title('Cистема вернёт ошибку, если неправильно указать логин или пароль')
    @allure.description(
        'Создаем курьера, логинимся под ним под неправильными паролем/логином, проверяем ошибку, удаляем курьера')
    def test_login_courier_incorrect_parameters(self, new_courier_parameters):
        couriers = CourierRoutes()
        couriers.create_courier(new_courier_parameters)
        courier_id = couriers.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        couriers.delete_courier(courier_id)
        response = couriers.login_courier(new_courier_parameters['login'],
                                         new_courier_parameters['password'])
        assert response.status_code == 404, f"Ошибка: ожидается статус ответа 404, но получили '{response.status_code}'"
        assert response.json()["message"] == Constants.ACCOUNT_NOT_FOUND_MSSG
