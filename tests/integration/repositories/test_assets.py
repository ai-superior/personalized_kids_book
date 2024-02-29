import pytest

from dependencies import DependencyInjector
from domain.assets.model import Asset
from domain.assets.repositories import AssetRepository


@pytest.mark.asyncio
async def test_get_all_assets(asset: Asset):
    repo: AssetRepository = DependencyInjector.get().assets()
    leads = await repo.list()
    assert len(leads) >= 1


@pytest.mark.asyncio
async def test_get_asset(asset: Asset):
    repo: AssetRepository = DependencyInjector.get().assets()
    lead_collection = await repo.get(asset.id)
    assert lead_collection.id == asset.id
