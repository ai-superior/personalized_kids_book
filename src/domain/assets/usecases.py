import abc

from domain.assets import queries, errors, commands
from domain.assets.model import Asset, AssetType, AssetStatus
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase


class StandardAssetUseCase(UseCase, abc.ABC):
    def __init__(self, messages: AssetRepository):
        super().__init__()
        self.messages = messages


class CreateAsset(UseCase):
    def __init__(self, assets: AssetRepository):
        super().__init__()
        self.assets = assets

    def execute(self, cmd: commands.CreateAsset):
        iterations = cmd.quantity
        assets = []
        for iteration in range(iterations):
            for asset_type in AssetType:
                asset = Asset(
                    order_id=cmd.order_id,
                    type=asset_type.value,
                    status=AssetStatus.PENDING.value,
                )
                assets.append(asset)
                self.assets.add(asset)
        return assets


class GetAsset(StandardAssetUseCase):
    def execute(self, query: queries.GetAsset) -> Asset:
        asset = self.messages.get(query.asset_id)

        if asset is None:  # pragma: no cover
            raise errors.AssetNotFound
        return asset


class GetAssetByOrderId(StandardAssetUseCase):
    def execute(self, query: queries.GetAssetByOrderId) -> list[Asset]:
        assets = self.messages.get_by_order_id(query.order_id)

        if assets is None:  # pragma: no cover
            raise errors.AssetNotFound
        return assets
