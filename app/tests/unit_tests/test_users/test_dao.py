from app.users.dao import UsersDAO
import pytest

USERS = [
    (1, "fedor@moloko.ru", True),
    (2, "sharik@moloko.ru", True),
    (9999, "test@test.ru", False),
]


@pytest.mark.parametrize("id, email, is_present", USERS)
async def test_find_user_by_id(id, email, is_present):
    user = await UsersDAO.find_by_id(id)
    if is_present:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user
