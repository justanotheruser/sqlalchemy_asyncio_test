import asyncio

from bot_types import FlightDirection
from config import config
from db import DB


async def main():
    db = DB(config)
    await db.start()
    await db.save_flight_direction(
        1, FlightDirection(start_code='ABC', start_name='AAAAAA', end_code='DEF', end_name='BBBBB',
                           with_transfer=True, departure_at='2023-06-01', return_at=None), price=10000)


if __name__ == '__main__':
    asyncio.run(main())
