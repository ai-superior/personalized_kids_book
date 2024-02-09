import abc
import secrets
from io import BytesIO

import requests
from PIL import Image, ImageDraw

from domain.assets.model import AssetType
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase
from domain.previews import queries, errors, commands
from domain.previews.model import Preview, PreviewStatus
from domain.previews.repositories import PreviewRepository
from settings import SETTINGS


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

    @staticmethod
    def fuse_images(cover_image_url, char_image_url, title, output_file_name):
        # Download the images
        cover_image = requests.get(cover_image_url)
        char_image = requests.get(char_image_url)

        # Open the images
        image1 = Image.open(BytesIO(cover_image.content))
        image2 = Image.open(BytesIO(char_image.content))

        # Resize the images to the same dimensions
        image1 = image1.resize(image2.size)

        # Overlay the text onto the first image
        draw = ImageDraw.Draw(image1)
        draw.text((10, 10), title, fill="black")

        # Blend the images together
        fused_image = Image.blend(image1, image2, alpha=0.5)

        fused_image.save(
            f"/home/subra/Documents/personalized_kids_book/public/results/{output_file_name}.jpg"
        )

        # Return the fused image
        return f"{SETTINGS.webserver.protocol}://{SETTINGS.webserver.host}:{SETTINGS.webserver.port}/public/results/{output_file_name}.jpg"

    def __init__(self, previews: PreviewRepository, assets: AssetRepository):
        super().__init__()
        self.previews = previews
        self.assets = assets

    def execute(self, cmd: commands.CreatePreview) -> Preview:
        assets = self.assets.get_by_order_id(cmd.order_id)
        # assets_for_preview = self.assets_for_preview(assets)
        assets_for_preview = assets

        # if cmd.asset_ids is None:
        #     asset_ids = [asset.id for asset in assets_for_preview]
        # else:
        #     asset_ids = cmd.asset_ids

        asset_ids = [asset.id for asset in assets_for_preview]
        char_image_url = [
            asset.value
            for asset in assets_for_preview
            if asset.type == AssetType.CHARACTER_IMAGE.value
        ][0]
        cover_image_url = [
            asset.value
            for asset in assets_for_preview
            if asset.type == AssetType.BACKGROUND_IMAGE.value
        ][0]
        title = [
            asset.value
            for asset in assets_for_preview
            if asset.type == AssetType.TITLE.value
        ][0]
        result_url = self.fuse_images(
            cover_image_url, char_image_url, title, secrets.token_hex(6)
        )

        preview = Preview(
            asset_ids=asset_ids,
            status=PreviewStatus.COMPLETED.value,
            is_approved=False,
            title=title,
            character_image_url=char_image_url,
            cover_image_url=cover_image_url,
            fused_image_url=result_url,
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
