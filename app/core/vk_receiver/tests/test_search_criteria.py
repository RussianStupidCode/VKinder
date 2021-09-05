import app.core.vk_receiver.search_criteria as criteria


def test_valid_age_criterion_success_1():
    min_age = 10
    max_age = 20
    try:
        criteria.AgeCriterion.validation(min_age, max_age, 1)
        assert True
    except:
        assert False


def test_valid_age_criterion_success_2():
    min_age = 10
    max_age = 10
    try:
        criteria.AgeCriterion.validation(min_age, max_age, 1)
        assert True
    except:
        assert False


def test_valid_age_criterion_fail_1():
    min_age = 10
    max_age = 9
    try:
        criteria.AgeCriterion.validation(min_age, max_age, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_age_criterion_fail_2():
    min_age = '10'
    max_age = 9
    try:
        criteria.AgeCriterion.validation(min_age, max_age, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_city_criterion_success_1():
    cities = 'Москва'
    try:
        criteria.CityCriterion.validation(cities, 1)
        assert True
    except:
        assert False


def test_valid_city_criterion_fail_1():
    cities = ['Сант-Петербург']
    try:
        criteria.CityCriterion.validation(cities, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_city_criterion_fail_2():
    cities = [1, 2]
    try:
        criteria.CityCriterion.validation(cities, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_sex_criterion_success_1():
    sex = '1'
    try:
        criteria.SexCriterion.validation(sex, 1)
        assert True
    except:
        assert False


def test_valid_sex_criterion_success_2():
    sex = 0
    try:
        criteria.SexCriterion.validation(sex, 1)
        assert True
    except:
        assert False


def test_valid_sex_criterion_fail_1():
    sex = '-1'
    try:
        criteria.SexCriterion.validation(sex, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_sex_criterion_fail_2():
    sex = 'male'
    try:
        criteria.SexCriterion.validation(sex, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_relation_criterion_success_1():
    relation = '1'
    try:
        criteria.RelationCriterion.validation(relation, 1)
        assert True
    except:
        assert False


def test_valid_relation_criterion_success_2():
    relation = '8'
    try:
        criteria.RelationCriterion.validation(relation, 1)
        assert True
    except:
        assert False


def test_valid_relation_criterion_fail_1():
    relation = '-1'
    try:
        criteria.RelationCriterion.validation(relation, 1)
        assert False
    except ValueError as er:
        assert True


def test_valid_relation_criterion_fail_2():
    relation = 'не женат'
    try:
        criteria.RelationCriterion.validation(relation, 1)
        assert False
    except ValueError as er:
        assert True
