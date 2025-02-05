class Constants:
    URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
    ORDER_RESPONSE_KEYS = ["address", "color", "comment", "courierId", "createdAt", "deliveryDate", "firstName", "id",
                           "lastName", "metroStation", "phone", "rentTime", "status", "track", "updatedAt"]
    CREATE_COURIER_NO_DATA_MSSG = 'Недостаточно данных для создания учетной записи'
    CREATE_COURIER_LOGIN_USED_MSSG = 'Этот логин уже используется. Попробуйте другой.'
    NO_COURIER_BY_ID_MSSG = "Курьера с таким id нет."
    INVALID_SYNTAX_MSSG = 'invalid input syntax for type integer:'
    NO_DATA_FOR_LOGIN_MSSG = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND_MSSG = "Учетная запись не найдена"
    ORDER_ID_NOT_EXIST_MSSG = "Заказа с таким id не существует"
    COURIER_ID_NOT_EXIST_MSSG = "Курьера с таким id не существует"
    NO_DATA_FOR_SEARCH = "Недостаточно данных для поиска"
    NOT_FOUND_MSSG = "Not Found."
    ORDER_NOT_FOUND_MSSG = "Заказ не найден"