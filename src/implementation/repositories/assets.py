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
    }


def _db_to_model(asset):
    return Asset(
        id=asset["id"],
        status=asset["status"],
        type=asset["type"],
        order_id=asset["order_id"],
        value=asset["value"],
        created_at=asset["created_at"],
    )


class AssetSqlRepository(AssetRepository, SqlRepository):
    def add(self, asset: Asset):
        return self.db["assets"].insert_one(_model_to_db(asset))

    def get(self, asset_id: str) -> Asset:
        return _db_to_model(self.db["assets"].find_one({"id": asset_id}))

    def get_by_order_id(self, order_id: str) -> list[Asset]:
        assets = self.db["assets"].find({"order_id": order_id})
        return [_db_to_model(msg) for msg in assets]

    def list(self) -> list[Asset]:
        assets = self.db["assets"].find({})
        return [_db_to_model(msg) for msg in assets]
