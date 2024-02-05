import abc

from pymongo import MongoClient

from settings import Settings


def get_mongo_db(settings: Settings):
    mongo_client = MongoClient(settings.mongo.mongo_client)  # type: ignore
    db = mongo_client[settings.mongo.db]
    return db


class SqlRepository(abc.ABC):
    def __init__(self, settings: Settings):
        self.db = get_mongo_db(settings)
