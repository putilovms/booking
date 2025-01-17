from datetime import date
from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotels


router = APIRouter(
    prefix="/hotels",
    tags=['Hotels and Rooms']
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{id}")
async def get_hotel(id: int) -> SHotel:
    hotel = await HotelDAO.find_by_id(id)
    # return SHotel.model_validate(hotel).model_dump_json()
    return hotel
