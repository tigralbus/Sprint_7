import allure
from conftest import new_courier_parameters
from constants import Constants
from courier_routes import CourierRoutes


class TestDeleteCourier:
    @allure.title('Курьера можно удалить')
    @allure.description('Создаем курьера, логинимся под ним, удаляем курьера, проверяем, что курьер удален')
    def test_delete_courier_possibility(self, new_courier_parameters):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        response_delete = courier.delete_courier(courier_id)
        assert response_delete.status_code == 200, f"Ошибка: ожидается статус ответа 200, но получили '{response_delete.status_code}'"
        assert response_delete.json()['ok'] == True

    @allure.title('Курьера не удалить если отправить запрос без id')
    @allure.description('Создаем курьера, логинимся под ним, удаляем курьера без id, проверяем ошибку, удаляем курьера')
    def test_delete_courier_without_id_impossible(self):
        courier = CourierRoutes()
        no_id = None
        response_delete = courier.delete_courier(no_id)
        assert response_delete.status_code == 500, f"Ошибка: ожидается статус ответа 500, но получили '{response_delete.status_code}'"
        assert response_delete.json()['message'] == f'{Constants.INVALID_SYNTAX_MSSG} "{no_id}"'

    @allure.title('Если отправить запрос с несуществующим id, вернётся ошибка')
    @allure.description(
        'Создаем курьера, логинимся под ним, удаляем курьера, удаляем курьера еще раз, проверяем ошибку')
    def test_delete_courier_not_existing_id_impossible(self, new_courier_parameters):
        courier = CourierRoutes()
        courier.create_courier(new_courier_parameters)
        courier_id = courier.login_courier_return_id(new_courier_parameters['login'],
                                                     new_courier_parameters['password'])
        courier.delete_courier(courier_id)
        response_delete = courier.delete_courier(courier_id)
        assert response_delete.status_code == 404, f"Ошибка: ожидается статус ответа 200, но получили '{response_delete.status_code}'"
        assert response_delete.json()['message'] == Constants.NO_COURIER_BY_ID_MSSG
