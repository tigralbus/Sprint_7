import random
import string

from order_routes import OrderRoutes


class RandomHelper:

    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    @staticmethod
    def random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
