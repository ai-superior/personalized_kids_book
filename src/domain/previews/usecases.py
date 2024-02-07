import abc

from domain.assets.model import AssetType
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase
from domain.previews import queries, errors, commands
from domain.previews.model import Preview, PreviewStatus
from domain.previews.repositories import PreviewRepository


class StandardPreviewUseCase(UseCase, abc.ABC):
    def __init__(self, messages: PreviewRepository):
        super().__init__()
        self.messages = messages


class CreatePreview(UseCase):
    @staticmethod
    def assets_for_preview(assets):
        assets_for_preview = []
        for asset_type in AssetType:
            for asset in assets:
                if asset.type == asset_type:
                    assets_for_preview.append(asset)
                    break
        return assets_for_preview

    def __init__(self, previews: PreviewRepository, assets: AssetRepository):
        super().__init__()
        self.previews = previews
        self.assets = assets

    def execute(self, cmd: commands.CreatePreview) -> Preview:
        assets = self.assets.get_by_order_id(cmd.order_id)
        assets_for_preview = self.assets_for_preview(assets)

        if cmd.asset_ids is None:
            asset_ids = [asset.id for asset in assets_for_preview]
        else:
            asset_ids = cmd.asset_ids

        preview = Preview(
            asset_ids=asset_ids, status=PreviewStatus.PENDING.value, is_approved=False
        )

        self.previews.add(preview)
        return preview


class GetPreview(StandardPreviewUseCase):
    def execute(self, query: queries.GetPreview) -> Preview:
        preview = self.messages.get(query.preview_id)

        if preview is None:  # pragma: no cover
            raise errors.PreviewNotFound
        return preview


class GetPreviewByOrderId(StandardPreviewUseCase):
    def execute(self, query: queries.GetPreviewByOrderId) -> list[Preview]:
        previews = self.messages.get_by_order_id(query.order_id)

        if previews is None:  # pragma: no cover
            raise errors.PreviewNotFound
        return previews
