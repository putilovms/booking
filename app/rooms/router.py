from datetime import date
from app.hotels.router import router
from app.rooms.dao import RoomDAO
from app.rooms.schemas import SRooms


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms
