from fastapi import Depends
from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SHotel(BaseModel):
    adress: str
    name: str
    stars: int


@app.post("bookings")
def add_booking(booking: SBooking):
    pass


class HotelsSearchArgs:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Optional[bool] = None,
                 stars: Optional[int] = Query(None, ge=1, le=5),):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars
        pass


@app.get('/hotels', response_model=list[SHotel])
def get_hotels(
    serch_args: HotelsSearchArgs = Depends()
):
    hotels = [
        {
            'adress': 'адрес 123',
            'name': 'Имя Отеля',
            'stars': 5,
        }
    ]
    return hotels
