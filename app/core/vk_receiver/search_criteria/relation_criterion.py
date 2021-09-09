from app.core.vk_receiver.search_criteria.criterion import Criterion
from app.core.vk_receiver.search_criteria.utils import required_to_str


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