from typing import Annotated, Any

from sqlalchemy import JSON, NullPool
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings as s

if s.MODE == 'TEST':
    DB_URL = f'postgresql+asyncpg://{s.TEST_DB_USER}:{s.TEST_DB_PASS}@{s.TEST_DB_HOST}:{s.TEST_DB_PORT}/{s.TEST_DB_NAME}'
    DB_PARAMS = {"poolclass": NullPool}
else:
    DB_URL = f'postgresql+asyncpg://{s.DB_USER}:{s.DB_PASS}@{s.DB_HOST}:{s.DB_PORT}/{s.DB_NAME}'
    DB_PARAMS = {}

engine = create_async_engine(DB_URL, **DB_PARAMS)

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {
        dict[str, Any]: JSON
    }
