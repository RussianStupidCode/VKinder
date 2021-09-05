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
