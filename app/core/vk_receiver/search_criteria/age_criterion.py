from app.core.vk_receiver.search_criteria.criterion import Criterion
from app.core.vk_receiver.search_criteria.utils import required_to_str


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