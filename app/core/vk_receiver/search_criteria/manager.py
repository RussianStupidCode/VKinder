from app.core.vk_receiver.search_criteria.all_criteria import (AgeCriterion, Criterion,
                                                               CityCriterion, RelationCriterion,
                                                               SexCriterion)


class CriteriaManager:
    """
    класс для критериев поиска
    """

    criteria_mapper = {
        'возраст': 'age',
        'пол': 'sex',
        'город': 'city',
        'статус': 'relation',
    }

    criteria_class = {
        'age': AgeCriterion,
        'sex': SexCriterion,
        'city': CityCriterion,
        'relation': RelationCriterion
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
        params = {
            'has_photo': 1,  # фото обязательно!
        }
        if self._possible_criteria['age'].is_required:
            params['age_from'] = self._possible_criteria['age'].min_age
            params['age_to'] = self._possible_criteria['age'].max_age

        if self._possible_criteria['relation'].is_required:
            params['relation'] = self._possible_criteria['relation'].value

        if self._possible_criteria['sex'].is_required:
            params['sex'] = self._possible_criteria['sex'].value

        if self._possible_criteria['city'].is_required:
            params['city'] = self._possible_criteria['city'].value

        return params