import allure
import requests
from conftest import new_courier_parameters
from constants import Constants


class CourierRoutes:
    @allure.step('Создать курьера')  # декоратор
    def create_courier(self, new_courier_parameters):
        response = requests.post(f"{Constants.URL}/courier", data=new_courier_parameters)
        return response

    @allure.step('Логин курьера')  # декоратор
    def login_courier(self, login, password):
        login_payload = {
            "login": login,
            "password": password,
        }
        response_login = requests.post(f"{Constants.URL}/courier/login",
                                       data=login_payload)
        return response_login

    @allure.step('Логин курьера для получения id')  # декоратор
    def login_courier_return_id(self, login, password):
        login_payload = {
            "login": login,
            "password": password,
        }
        response_login = requests.post(f"{Constants.URL}/courier/login", data=login_payload)
        return response_login.json()['id']

    @allure.step('Удалить курьера')
    def delete_courier(self, courier_id):
        response_delete = requests.delete(f"https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}")
        return response_delete
