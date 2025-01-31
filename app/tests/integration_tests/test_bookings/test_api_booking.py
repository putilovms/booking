import pytest
from httpx import AsyncClient

BOOKINGS = [
    *[(4, "2030-05-01", "2030-05-01", 200)] * 8,
    (4, "2030-05-01", "2030-05-01", 409)
]


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", BOOKINGS)
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to,
    })
    assert response.status_code == status_code
