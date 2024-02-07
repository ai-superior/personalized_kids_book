from dependencies import DependencyInjector

from domain.assets.model import Asset
from domain.assets.repositories import AssetRepository


def test_get_all_assets(asset: Asset):
    repo: AssetRepository = DependencyInjector.get().assets()
    leads = repo.list()
    assert len(leads) >= 1


def test_get_asset(asset: Asset):
    repo: AssetRepository = DependencyInjector.get().assets()
    lead_collection = repo.get(asset.id)
    assert lead_collection.id == asset.id
