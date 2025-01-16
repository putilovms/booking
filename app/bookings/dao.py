from datetime import date
from app.database import engine, async_session_maker
from sqlalchemy import and_, func, insert, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
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
