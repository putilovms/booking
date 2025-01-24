from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.rooms.router import router as router_rooms
from app.users.models import Users
from app.users.router import router as router_users

origins = [
    'http://localhost:3000',
]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Список разрешённых адресов
    allow_credentials=True,  # Разрешить куки
    # Список разрешённых запросов
    allow_methods=["GET", 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    # Список разрешённых заголовков
    allow_headers=[
        'Content-Type',
        'Set-Cookie',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin',
        'Authorization'
    ],
)

app.mount('/static', StaticFiles(directory='app/static'), "static")

app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_images)

admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend
)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
