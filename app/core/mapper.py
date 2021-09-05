from app.core.db.tables import Person
from app.core.vk_receiver import VkUser


class Mapper:

    @staticmethod
    def vk_user_to_person(user: VkUser):
        return Person(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            age=user.age,
            gender=user.gender,
            relation_status=user.relation,
            city=user.city
        )

    @staticmethod
    def person_to_vk_user(person: Person):
        user = VkUser.create_user(**{
            'id': person.id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'city': person.city,
            'gender': person.gender,
            'relation': person.relation_status,
            'age': person.age
        })
        for photo in person.photos:
            user.photos.append({'url': photo.url, 'likes': 0})
        return user
