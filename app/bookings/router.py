from datetime import date

from fastapi import APIRouter, Depends, status

import app.exceptions as excep
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingAdd
from app.tasks.tasks import send_booking_confirmation_email
from app.users.auth import get_current_user
from app.users.models import Users
from fastapi_versioning import version

router = APIRouter(
    prefix="/bookings",
    tags=['Bookings']
)


@router.get('')
async def get_bookings(
    user: Users = Depends(get_current_user)
) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
@version(1)
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise excep.RoomCannotBeBooked
    booking_dict = SBookingAdd.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    id: int,
    user: Users = Depends(get_current_user)
):
    result = await BookingDAO.delete(id=id, user_id=user.id)
    if not result:
        raise excep.BookingCannotBeDeleted
    return {"message": "Resource deleted successfully"}


@router.get("/all")
async def get_hotels_all():
    bookings = await BookingDAO._find_all()
    return bookings
