import allure
import requests

from constants import Constants


class OrderRoutes:
    @allure.step('Создать заказ')
    def create_order(self, new_order_parameters):
        response = requests.post(f"{Constants.URL}/orders", data=new_order_parameters)
        return response

    @allure.step('Отменить заказ')
    def cancel_order(self, track):
        response = requests.put(f"{Constants.URL}/orders/cancel", params=track)
        return response

    @allure.step('Получить заказ по его номеру')
    def get_order_by_track(self, track):
        response = requests.get(f"{Constants.URL}/orders/track", params=track)
        return response

    @allure.step('Получить заказ по его номеру')
    def get_orders_list(self, orders_list_parameters):
        response = requests.get(f'{Constants.URL}/orders', params=orders_list_parameters)
        return response

    @allure.step('Принять заказ')
    def accept_order(self, courier_id, order_id):
        response = requests.put(f"{Constants.URL}/orders/accept/{order_id}", params=courier_id)
        return response
