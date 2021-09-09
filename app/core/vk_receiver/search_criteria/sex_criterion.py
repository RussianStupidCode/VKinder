from app.core.vk_receiver.search_criteria.criterion import Criterion
from app.core.vk_receiver.search_criteria.utils import required_to_str


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
