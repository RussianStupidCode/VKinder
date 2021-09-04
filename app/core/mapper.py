from app.db.tables import Photo, Person
from app.vk_receiver.vk_user import VkUser


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
        return VkUser.create_user(**{
            'id': person.id,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'city': person.city,
            'gender': person.gender,
            'relation': person.relation_status,
            'age': person.age
        })