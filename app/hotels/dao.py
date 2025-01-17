from datetime import date
from app.hotels.models import Hotels
from app.dao.base import BaseDAO
from app.database import engine, async_session_maker
from sqlalchemy import and_, func, insert, or_, select
from app.bookings.models import Bookings
from app.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # Получить комнат отеля
            '''
            with booked_rooms as (
                select * from bookings where
                (date_from >= '2025-01-15' and date_from <= '2025-01-20') or
                (date_from <= '2025-01-15' and date_to > '2025-01-15')
            )

            select 
                hotels.id, 
                hotels."name",
                hotels.location,
                hotels.services,
                hotels.rooms_quantity,
                hotels.image_id,
                hotels.rooms_quantity - count(booked_rooms.room_id) as rooms_left
            from hotels 
            join rooms on hotels.id = rooms.hotel_id 
            left join booked_rooms on booked_rooms.room_id = rooms.id 
            where hotels.location iLIKE '%алтай%' 
            group by 
                hotels.id, 
                hotels.rooms_quantity
            '''
            booked_rooms = select(Bookings).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            ).cte("booked_rooms")
            get_hotels = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                func.coalesce(
                    Hotels.rooms_quantity -
                    func.count(booked_rooms.c.room_id), 0
                ).label("rooms_left")
            ).select_from(Hotels).join(
                Rooms, Hotels.id == Rooms.hotel_id
            ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Hotels.location.icontains(location)
                    ).group_by(
                Hotels.id, Hotels.rooms_quantity
            )
            hotels = await session.execute(get_hotels)
            hotels = hotels.mappings().all()
            available_hotels = list(
                filter(lambda a: a['rooms_left'] > 0, hotels))
            return (available_hotels)
