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
        "was_shown": assets.was_shown,
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

    async def update_was_shown_flag(self, asset_id: str):
        return await self.db["assets"].update_one(
            {"id": asset_id}, {"$set": {"was_shown": True}}
        )

    async def get_by_order_id(self, order_id: str) -> list[Asset]:
        cursor = self.db["assets"].find({"order_id": order_id})
        assets = []
        async for document in cursor:
            if document["was_shown"] is not True:
                await self.update_was_shown_flag(document["id"])
            assets.append(_db_to_model(document))
        return assets

    async def list(self) -> list[Asset]:
        cursor = self.db["assets"].find({})
        assets = []
        for document in cursor:
            assets.append(_db_to_model(document))
        return assets
