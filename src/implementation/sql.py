import abc
import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from settings import Settings


def get_async_mongo_db(settings: Settings):
    loop = asyncio.get_event_loop()
    mongo_client = AsyncIOMotorClient(settings.mongo.mongo_client, io_loop=loop)  # type: ignore
    db = mongo_client[settings.mongo.db]
    return db


class SqlRepository(abc.ABC):
    def __init__(self, settings: Settings):
        self.db = get_async_mongo_db(settings)
