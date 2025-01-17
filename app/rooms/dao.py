from datetime import date
from app.bookings.models import Bookings
from app.rooms.models import Rooms
from app.dao.base import BaseDAO
from app.database import engine, async_session_maker
from sqlalchemy import and_, func, insert, or_, select


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            '''
            with booked_rooms as (
                select * from bookings where
                (date_from >= '2025-01-15' and date_from <= '2025-01-20') or
                (date_from <= '2025-01-15' and date_to > '2025-01-15')
            )
            select
                rooms.id,
                rooms.hotel_id,
                rooms.name,
                rooms.description,
                rooms.price,
                rooms.services,
                rooms.quantity,
                rooms.image_id,
                rooms.price * EXTRACT(DAY FROM '2025-01-20'::timestamp - '2025-01-15'::timestamp) as total_cost,
                rooms.quantity - count(booked_rooms.room_id) as rooms_left
            from rooms
            left join booked_rooms on booked_rooms.room_id = rooms.id 
            where rooms.hotel_id = 1
            group by rooms.id, booked_rooms.room_id
            '''
            duration = date_to - date_from
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
            get_rooms = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.price,
                Rooms.services,
                Rooms.quantity,
                Rooms.image_id,
                func.coalesce(
                    Rooms.price * duration.days, 0
                ).label("total_cost"),
                func.coalesce(
                    Rooms.quantity -
                    func.count(booked_rooms.c.room_id), 0
                ).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.hotel_id == hotel_id
                    ).group_by(
                Rooms.id, booked_rooms.c.room_id
            )
            rooms = await session.execute(get_rooms)
            rooms = rooms.mappings().all()
            return rooms
