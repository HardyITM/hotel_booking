from contextlib import asynccontextmanager
import time

import uvicorn
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI, version

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.db import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger

from app.config import settings as s

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{s.REDIS_URL}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        "Request handling time",
        extra={
            "process_time": round(process_time, 4)
        }
    )
    return response

sentry_sdk.init(
    dsn="https://98c4fb0a1b006611e37d6666aa2e85f1@o4507136306905088.ingest.de.sentry.io/4507136805699664",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory='app/static'), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
