
class Criterion:
    possible_values = {}

    def __init__(self, value=None, weight=1, is_required=False):
        self._value = value
        self._weight = weight
        self._is_required = is_required

    @classmethod
    def possible_value_to_str(cls):
        result = ""
        for key, value in cls.possible_values.items():
            result += f'{key}: {value}\n'
        return result

    @classmethod
    def validation(cls, value):
        pass

    @property
    def is_required(self):
        return  self._is_required

    def is_agree(self, value):
        """подходит ли величина по критерию"""
        return value == self._value

    def get_weight(self, value):
        if self.is_agree(value):
            return self._weight
        return 0

    def __str__(self):
        result = f'{self.__doc__} Возможные значения: \n'
        result += self.__class__.possible_value_to_str()
        return result


class AgeCriterion(Criterion):
    def __init__(self, min_age=0, max_age=9999, weight=1, is_required=False):
        super().__init__(None, weight, is_required)
        self.__min_age = min_age
        self.__max_age = max_age

    def is_agree(self, value):
        if value is None:
            return False

        return self.__min_age <= value <= self.__max_age

    @classmethod
    def validation(cls, min_age, max_age):
        try:
            min_age = int(min_age)
            max_age = int(max_age)
        except:
            raise ValueError("Возраст должен быть целым неотрицательным числом")

        if min_age < 0 or max_age < 0:
            raise ValueError("Возраст не может быт отрицательным")
        if max_age < min_age:
            raise ValueError("Максимальный возраст меньше минимального")


class SexCriterion(Criterion):
    """Пол"""

    possible_values = {
        1: 'женщина',
        2: 'мужчина',
        0: 'не указан'
    }

    def __init__(self, value=None, weight=1, is_required=False):
        super().__init__(value, weight, is_required)

    @classmethod
    def validation(cls, value):
        try:
            value = int(value)
        except:
            raise ValueError(f"Пол должен быть целым числом \n{cls.possible_value_to_str()}")

        if value not in cls.possible_values:
            raise ValueError(f"Нет такого допустимого значения \n{cls.possible_value_to_str()}")


class RelationCriterion(Criterion):
    """Семейное положение"""

    possible_values = {
        1: 'не женат/не замужем',
        2: 'есть друг/есть подруга',
        3: 'помолвлен/помолвлена',
        4: 'женат/замужем',
        5: 'всё сложно',
        6: 'в активном поиске',
        7: 'влюблён/влюблена',
        8: 'в гражданском браке',
        0: 'не указано'
    }

    def __init__(self, value=None, weight=1, is_required=False):
        super().__init__(value, weight, is_required)

    @classmethod
    def validation(cls, value):
        try:
            value = int(value)
        except:
            raise ValueError(f"Семейное положение должно быть целым числом \n{cls.possible_value_to_str()}")

        if value not in cls.possible_values:
            raise ValueError(f"Нет такого допустимого значения \n{cls.possible_value_to_str()}")


class CityCriterion(Criterion):

    def __init__(self, value: list = None, weight=1, is_required=False):
        value = [v.lower() for v in value]
        super().__init__(value, weight, is_required)

    def is_agree(self, value):
        return value.lower() in self._value

    @classmethod
    def validation(cls, value):
        if not isinstance(value, list) or not all([isinstance(v, str) for v in value]):
            raise ValueError('Значение критерия городов должно быть списком городов')


class CriteriaManager:
    """
    класс для критериев поиска
    """

    criteria_mapper = {
        'возраст': 'age',
        'пол': 'sex',
        'город': 'city',
        'статус': 'status',
    }

    def __init__(self):
        """
            - у каждого критерия помимо значения есть вес и флаг обязательности
            - значения соответствуют значениям из vk_api
        """

        self.possible_criteria = {
            'age': AgeCriterion(),
            'sex': SexCriterion(0),
            'city': CityCriterion(['']),
            'relation': RelationCriterion(0)
        }

    def is_all_criteria_not_required(self):
        for value in self.possible_criteria.values():
            if value.is_required:
                return False
        return True
