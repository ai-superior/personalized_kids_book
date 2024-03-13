from dependency_injector import containers
from dependency_injector.providers import Factory, Object

from domain.assets.repositories import AssetRepository
from domain.orders.repositories import OrderRepository
from domain.orders.services import LLMProcessor, CRM
from domain.previews.repositories import PreviewRepository
from implementation.repositories.assets import AssetSqlRepository
from implementation.repositories.orders import OrderSqlRepository
from implementation.repositories.previews import PreviewSqlRepository
from implementation.services.hubspot import HubSpot
from implementation.services.open_ai import OpenAIAPI
from settings import SETTINGS, Settings


class DependencyInjector(containers.DeclarativeContainer):
    _instance = None
    config: Object[Settings] = Object(SETTINGS)
    orders: Factory[OrderRepository] = Factory(OrderSqlRepository, config)
    assets: Factory[AssetRepository] = Factory(AssetSqlRepository, config)
    previews: Factory[PreviewRepository] = Factory(PreviewSqlRepository, config)
    crm: Factory[CRM] = Factory(HubSpot)
    gpt: Factory[LLMProcessor] = Factory(OpenAIAPI)

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = DependencyInjector()
        return cls._instance
