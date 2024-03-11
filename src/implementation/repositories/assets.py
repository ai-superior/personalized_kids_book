from domain.assets import model
from domain.assets.model import Asset
from domain.assets.repositories import AssetRepository
from implementation.sql import SqlRepository


def _model_to_db(assets: model.Asset):
    return {
        "id": assets.id,
        "type": assets.type.value,
        "order_id": assets.order_id,
        "status": assets.status.value,
        "created_at": assets.created_at,
        "value": assets.value,
        "prompt": assets.prompt,
        "revised_cover_prompt": assets.revised_cover_prompt,
        "category": assets.category.value if assets.category else None,
    }


def _db_to_model(asset):
    if "_id" in asset:
        del asset["_id"]
    return Asset.from_dict(asset)


class AssetSqlRepository(AssetRepository, SqlRepository):
    async def add(self, asset: Asset):
        return await self.db["assets"].insert_one(_model_to_db(asset))

    async def get(self, asset_id: str) -> Asset:
        document = await self.db["assets"].find_one({"id": asset_id})
        return _db_to_model(document)

    async def get_by_order_id(self, order_id: str) -> list[Asset]:
        cursor = self.db["assets"].find({"order_id": order_id})
        assets = []
        async for document in cursor:
            assets.append(_db_to_model(document))
        return assets

    async def list(self) -> list[Asset]:
        cursor = self.db["assets"].find({})
        assets = []
        async for document in cursor:
            assets.append(_db_to_model(document))
        return assets
