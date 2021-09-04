def get_vk_user_age(bdate):
    age = None
    if bdate and len(bdate.split()) == 3:
        age = bdate.split()[2]

    return age


def get_vk_user_city(city: dict) -> str:
    if city is None:
        return ''
    return city['title']