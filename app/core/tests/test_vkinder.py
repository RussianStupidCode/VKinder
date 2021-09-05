import pytest
from app.core.vkinder import VkInder, VkReceiver
from app.core.vk_receiver.search_criteria import CriteriaManager, AgeCriterion, CityCriterion, SexCriterion, RelationCriterion

def criteria():
    criteria = CriteriaManager()
    possible_criteria = {
        'age': AgeCriterion(),
        'sex': SexCriterion(1),
        'city': CityCriterion('Екатеринбург'),
        'relation': RelationCriterion(6)
    }
    criteria.set_possible_criteria(possible_criteria)
    return criteria


@pytest.fixture()
def receiver():
    return VkInder(VkReceiver(), criteria())


def test_get_vk_user_list(receiver: VkInder):
    users, last_idx = receiver.get_vk_user_list()
    assert len(users) > 0
    assert last_idx > 0
    assert len(receiver.saving_user_id) > 0
