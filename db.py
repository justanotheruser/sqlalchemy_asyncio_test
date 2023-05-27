import logging
import typing
from contextlib import contextmanager
from typing import Optional, Any

from bot_types import FlightDirectionFull, FlightDirection
from config import BotConfig
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Boolean
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker

class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserFlightDirection(Base):
    __tablename__ = "flight_direction"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    start_code: Mapped[str]
    start_name: Mapped[str]
    end_code: Mapped[str]
    end_name: Mapped[str]
    price: Mapped[Optional[int]]
    with_transfer: Mapped[bool]
    departure_at: Mapped[str]
    return_at: Mapped[Optional[str]]


class DB:
    def __init__(self, config: BotConfig):
        username = config.db_user
        password = config.db_pass.get_secret_value()
        host = config.db_host
        dbname = config.db_name
        self.engine = create_async_engine(
            f"mysql+asyncmy://{username}:{password}@{host}/{dbname}",
            echo=True,
        )

    async def start(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save_flight_direction(self, user_id: int, direction: FlightDirection, price: int):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                session.add_all(
                    [
                        UserFlightDirection(user_id=user_id, start_code=direction.start_code,
                                            start_name=direction.start_name, end_code=direction.end_code,
                                            end_name=direction.end_name, price=price,
                                            with_transfer=direction.with_transfer,
                                            departure_at=direction.departure_at,
                                            return_at=direction.return_at)
                    ]
                )

    async def graceful_shutdown(self):
        print('Graceful shutdown of DB engine')
        await self.engine.dispose()
