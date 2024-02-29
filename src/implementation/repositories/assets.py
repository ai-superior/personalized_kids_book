from domain.assets import model
from domain.assets.model import Asset
from domain.assets.repositories import AssetRepository
from implementation.sql import SqlRepository


def _model_to_db(assets: model.Asset):
    return {
        "id": assets.id,
        "type": assets.type,
        "order_id": assets.order_id,
        "status": assets.status,
        "created_at": assets.created_at,
        "value": assets.value,
        "prompt": assets.prompt,
    }


def _db_to_model(asset):
    return Asset(
        id=asset["id"],
        status=asset["status"],
        prompt=asset["prompt"],
        type=asset["type"],
        order_id=asset["order_id"],
        value=asset["value"],
        created_at=asset["created_at"],
    )


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
