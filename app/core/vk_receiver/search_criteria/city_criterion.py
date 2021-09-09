from app.core.vk_receiver.search_criteria.criterion import Criterion
from app.core.vk_receiver.search_criteria.utils import required_to_str

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