def required_to_str(boolean):
    if boolean:
        return 'обяательный'
    return 'необязательный'


class Criterion:
    possible_values = {}

    def __init__(self, value=None, weight=1, is_required=False):
        self._value = value
        self._weight = weight
        self._is_required = is_required

    @property
    def value(self):
        return self._value

    @staticmethod
    def raise_weight(weight):
        try:
            weight = float(weight)
            if weight < 0:
                raise Exception
        except:
            raise ValueError('Вес критерия должен быть положительным числом')

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
        return self._is_required

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
        super().__init__(None, float(weight), is_required)
        self.__min_age = int(min_age)
        self.__max_age = int(max_age)

    @property
    def min_age(self):
        return self.__min_age

    @property
    def max_age(self):
        return self.__max_age

    def is_agree(self, value):
        if value is None:
            return False

        return self.__min_age <= value <= self.__max_age

    @classmethod
    def validation(cls, min_age, max_age, weight):
        Criterion.raise_weight(weight)
        try:
            min_age = int(min_age)
            max_age = int(max_age)
        except:
            raise ValueError("Возраст должен быть целым неотрицательным числом")

        if min_age < 0 or max_age < 0:
            raise ValueError("Возраст не может быт отрицательным")
        if max_age < min_age:
            raise ValueError("Максимальный возраст меньше минимального")

    def __str__(self):
        return f'Возраст: от {self.min_age} до {self.max_age} |' \
               f' {required_to_str(self.is_required)} | вес {self._weight}'


class SexCriterion(Criterion):
    """Пол"""

    possible_values = {
        1: 'женщина',
        2: 'мужчина',
        0: 'не указан'
    }

    def __init__(self, value=None, weight=1, is_required=False):
        super().__init__(int(value), float(weight), is_required)

    @classmethod
    def validation(cls, value, weight):
        Criterion.raise_weight(weight)
        try:
            value = int(value)
        except:
            raise ValueError(f"Пол должен быть целым числом \n{cls.possible_value_to_str()}")

        if value not in cls.possible_values:
            raise ValueError(f"Нет такого допустимого значения \n{cls.possible_value_to_str()}")

    def __str__(self):
        return f'Пол: {SexCriterion.possible_values[self.value]} | {required_to_str(self.is_required)} ' \
               f'| вес {self._weight}'


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
        super().__init__(int(value), float(weight), is_required)

    @classmethod
    def validation(cls, value, weight):
        Criterion.raise_weight(weight)
        try:
            value = int(value)
        except:
            raise ValueError(f"Семейное положение должно быть целым числом \n{cls.possible_value_to_str()}")

        if value not in cls.possible_values:
            raise ValueError(f"Нет такого допустимого значения \n{cls.possible_value_to_str()}")

    def __str__(self):
        return f'Статус отношений: {RelationCriterion.possible_values[self.value]} ' \
               f'| {required_to_str(self.is_required)}  | вес {self._weight}'


class CityCriterion(Criterion):

    def __init__(self, value: str = None, weight=1, is_required=False):
        super().__init__(value, float(weight), is_required)

    def is_agree(self, value):
        return value.lower() == self._value.lower()

    def __str__(self):
        return f'Город: {self.value} | {required_to_str(self.is_required)} | вес {self._weight}'

    @classmethod
    def validation(cls, value, weight):
        Criterion.raise_weight(weight)
        if not isinstance(value, str):
            raise ValueError('Критерий города должно быть строкой')


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

        self._possible_criteria = {
            'age': AgeCriterion(),
            'sex': SexCriterion(1),
            'city': CityCriterion('Екатеринбург', is_required=True),
            'relation': RelationCriterion(6, is_required=True)
        }

    def is_all_criteria_not_required(self):
        for value in self._possible_criteria.values():
            if value.is_required:
                return False
        return True

    def get_criterion(self, key):
        return self._possible_criteria[key]

    @property
    def criteria(self):
        return self._possible_criteria

    def change_criterion(self, name, criterion: Criterion):
        self._possible_criteria[name] = criterion

    def set_possible_criteria(self, possible_criteria):
        self._possible_criteria = possible_criteria

    def return_vk_params(self):
        return {
            'age_from': self._possible_criteria['age'].min_age,
            'age_to': self._possible_criteria['age'].max_age,
            'has_photo': 1,  # фото обязательно!
            'relation': self._possible_criteria['relation'].value,
            'sex': self._possible_criteria['sex'].value,
            'city': self._possible_criteria['city'].value
        }



