from httpx import AsyncClient
import pytest

REGISTER_USER = [
    ("kot@pes.com", "test", 200),
    ("kot@pes.com", "kotopes", 409),
    ("12345", "12345", 422),
]

@pytest.mark.parametrize("email, password, status", REGISTER_USER)
async def test_register_user(email, password, status, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status
