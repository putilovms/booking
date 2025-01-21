from datetime import date

from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(Bookings.room_id == room_id,
                     or_(
                         and_(
                             Bookings.date_from >= date_from,
                             Bookings.date_from <= date_to
                         ),
                         and_(
                             Bookings.date_from <= date_from,
                             Bookings.date_to > date_from
                         )
                     ))
            ).cte("booked_rooms")
            get_room_left = select(
                Rooms.quantity - func.count(booked_rooms.c.room_id)
            ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            # print(get_room_left.compile(
            #     engine, compile_kwargs={"literal_binds": True}))
            room_left_count = await session.execute(get_room_left)
            room_left_count: int = room_left_count.scalar()
            if room_left_count > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            '''
            select
                bookings.room_id,
                bookings.user_id,
                bookings.date_from,
                bookings.date_to,
                bookings.price,
                bookings.total_cost,
                bookings.total_days,
                rooms.image_id,
                rooms.name,
                rooms.description,
                rooms.services
            from bookings
            join rooms on bookings.room_id = rooms.id 
            where user_id = 3
            '''
            query = select(
                Bookings.room_id,
                Bookings.user_id,
                Bookings.date_from,
                Bookings.date_to,
                Bookings.price,
                Bookings.total_cost,
                Bookings.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).select_from(
                Bookings
            ).join(
                Rooms, Bookings.room_id == Rooms.id
            ).where(
                Bookings.user_id == user_id
            )
            bookings = await session.execute(query)
            return bookings.mappings().all()
