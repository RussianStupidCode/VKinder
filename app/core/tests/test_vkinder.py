import pytest
from app.core.vkinder import VkInder


@pytest.fixture()
def receiver():
    return VkInder()


def test_get_vk_user_list(receiver: VkInder):
    users, last_idx = receiver.get_vk_user_list()
    assert len(users) > 0
    assert last_idx > 0
    assert len(receiver.saving_user_id) > 0
