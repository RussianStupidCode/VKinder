import sqlalchemy.exc

from db.tests.connect import session
from db.tables import Person, Photo, Interest


def test_add_person(session):
    p1 = Person(
        id=123456,
        first_name="f_1",
        last_name='l_1',
        age=21,
        url='http//',
        gender='male',
        status='free',
        city='ekb'
    )

    p2 = Person(
        id=123457,
        first_name="f_1",
        last_name='l_1',
        age=21,
        url='http//',
        gender='male',
        status='free',
        city='moscow'
    )

    session.add(p1)
    p1.persons.append(p2)
    session.commit()

    assert session.query(Person).filter_by(id=123456).first().city == 'ekb'
    assert session.query(Person).filter_by(id=123457).first().city == 'moscow'
    assert len(p1.persons) == 1


def test_add_person_repeat(session):
    p1 = Person(
        id=123456,
        first_name="f_1",
        last_name='l_1',
        age=21,
        url='http//',
        gender='male',
        status='free',
        city='ekb'
    )

    p2 = Person(
        id=123457,
        first_name="f_1",
        last_name='l_1',
        age=21,
        url='http//',
        gender='male',
        status='free',
        city='moscow'
    )

    session.add(p1)
    p1.persons.append(p2)
    p1.persons.append(p2)
    try:
        session.commit()
        assert False
    except sqlalchemy.exc.IntegrityError:
        assert True


def test_add_interest(session):
    interest = Interest(name='Плавание')
    person = Person(
        id=123456,
        first_name="f_1",
        last_name='l_1',
        age=21,
        url='http//',
        gender='male',
        status='free',
        city='ekb'
    )

    session.add(interest)
    interest.persons.append(person)
    session.commit()

    assert session.query(Person).first().id == 123456
    assert person.interests[0].name == 'Плавание'


def test_add_photo(session):
    person = Person(
        id=123456,
        first_name="f_1",
        last_name='l_1',
        age=21,
        url='http//',
        gender='male',
        status='free',
        city='ekb'
    )

    photo_1 = Photo(
        url='http//gfg'
    )

    session.add(person)
    person.photos.append(photo_1)
    session.commit()

    assert session.query(Photo).first().url == 'http//gfg'
    assert session.query(Photo).first().owner_id == person.id
