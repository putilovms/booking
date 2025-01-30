from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request
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
from app.prometheus.router import router as router_prometheus
from app.logger import logger

from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator

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


app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_prometheus)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response

app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
Instrumentator().instrument(app).expose(app)

admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend
)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

app.mount('/static', StaticFiles(directory='app/static'), "static")
