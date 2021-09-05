from app.db.tables import Photo, Person
from app.vk_receiver.vk_user import VkUser
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

    def suitable_users_save(self, main_user: VkUser, suitable_user: VkUser,  suitable_photos=None):
        person = self.get_person(id=main_user.id)
        if person is None:
            self.user_save(main_user)
            person = self.get_person(id=main_user.id)

        suitable_person = Mapper.vk_user_to_person(suitable_user)
        person.persons.append(suitable_person)

        if suitable_photos is not None:
            photos = [Photo(url=p['url']) for p in suitable_photos]
            suitable_person.photos.extend(photos)
        self._session.commit()
