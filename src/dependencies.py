from dependency_injector import containers
from dependency_injector.providers import Factory, Object

from domain.orders.repositories import OrderRepository
from domain.orders.services import LLMProcessor
from implementation.repositories.orders import OrderSqlRepository
from implementation.services.open_ai import OpenAIAPI
from settings import SETTINGS, Settings


class DependencyInjector(containers.DeclarativeContainer):
    _instance = None
    config: Object[Settings] = Object(SETTINGS)
    orders: Factory[OrderRepository] = Factory(OrderSqlRepository, config)
    gpt: Factory[LLMProcessor] = Factory(OpenAIAPI)

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = DependencyInjector()
        return cls._instance
