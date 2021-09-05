from app.core.db.tables import Photo, Person
from app.core.vk_receiver import VkUser
from app.core.mapper import Mapper


class DbExchanger:
    def __init__(self, session):
        self._session = session

    def user_save(self, user: VkUser):
        person = Mapper.vk_user_to_person(user)
        self._session.add(person)
        self._session.commit()

    def get_person(self, id):
        person = self._session.query(Person).filter_by(id=id).first()
        return person

    def get_favorites(self, id):
        """возвращает список свзязанных пользователей"""
        person = self._session.query(Person).filter_by(id=id).first()
        return [Mapper.person_to_vk_user(p) for p in person.persons]

    def suitable_users_save(self, main_user: VkUser, suitable_user: VkUser):
        person = self.get_person(id=main_user.id)
        if person is None:
            self.user_save(main_user)
            person = self.get_person(id=main_user.id)

        suitable_person = Mapper.vk_user_to_person(suitable_user)
        person.persons.append(suitable_person)

        if suitable_user.photos is not None:
            photos = [Photo(url=p['url']) for p in suitable_user.photos]
            suitable_person.photos.extend(photos)
        self._session.commit()
