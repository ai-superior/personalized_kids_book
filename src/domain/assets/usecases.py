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
        assets = []
        for _ in range(cmd.no_of_titles):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE.value,
                status=AssetStatus.PENDING.value,
            )
            assets.append(asset)
            self.assets.add(asset)

        for _ in range(cmd.no_of_cover_images):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.BACKGROUND_IMAGE.value,
                status=AssetStatus.PENDING.value,
            )
            assets.append(asset)
            self.assets.add(asset)

        asset = Asset(
            order_id=cmd.order_id,
            type=AssetType.CHARACTER_IMAGE.value,
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
