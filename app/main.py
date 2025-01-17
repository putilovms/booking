from fastapi import FastAPI, Query
from typing import Optional
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost:3000',
]

app = FastAPI()

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
