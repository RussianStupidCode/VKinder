from app.core.vk_receiver.search_criteria import (AgeCriterion,
                                                  SexCriterion,
                                                  CityCriterion,
                                                  RelationCriterion)
from app.frontend.console.utils import get_user_input
from app.core.config import DEBUG


def get_criteria(criterion_class, *args):
    weight = get_user_input('Введите вес критерия (положительное число)')

    is_required = get_user_input('Обязателный? да/нет')
    if 'да' in is_required:
        is_required = True
    else:
        is_required = False

    criterion_class.validation(*args, weight)
    criterion = criterion_class(*args, weight, is_required)
    return criterion


def change_criterion(value, criterion_class, key, criteria):
    try:
        if isinstance(value, tuple):
            criterion = get_criteria(criterion_class, value[0], value[1])
        else:
            criterion = get_criteria(criterion_class, value)
        criteria.change_criterion(key, criterion)
    except ValueError as e:
        if DEBUG:
            print(e)
        else:
            print('Ошибка введены некорректные данные')


class CriteriaCommandHandler:
    """класс для изменения критериев пользователем"""

    def __init__(self, criteria):
        self._criteria = criteria
        self._criteria_name = {
            'пол': 'sex',
            'возраст': 'age',
            'город': 'city',
            'статус': 'relation'
        }

        self._command_change = {
            'sex': self._change_sex,
            'age': self._change_age,
            'relation': self._change_relation,
            'city': self._change_city
        }

    def change_criterion(self):
        print(f'Список критериев: {list(self._criteria_name.keys())}')

        criterion_name = get_user_input('Введите название критерия').lower()
        if criterion_name not in self._criteria_name:
            print(f'Ошибка нет критерия {criterion_name} в списке {self._criteria_name.keys()}')
            return
        command = self._command_change[self._criteria_name[criterion_name]]
        command()

    def _change_age(self):
        min_age = get_user_input('Введите старт диапазона (от)')
        max_age = get_user_input('Введите старт диапазона (до)')
        change_criterion((min_age, max_age), AgeCriterion, 'age', self._criteria)

    def _change_city(self):
        city = get_user_input('Введите город')
        change_criterion(city, CityCriterion, 'city', self._criteria)

    def _change_relation(self):
        print(RelationCriterion.possible_value_to_str())
        relation = get_user_input('Введите статус отношений')
        change_criterion(relation, RelationCriterion, 'relation', self._criteria)

    def _change_sex(self):
        print(SexCriterion.possible_value_to_str())
        sex = get_user_input('Введите пол')
        change_criterion(sex, SexCriterion, 'sex', self._criteria)