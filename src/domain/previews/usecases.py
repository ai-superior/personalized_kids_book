import abc
import asyncio
import json
import secrets
from io import BytesIO
from textwrap import TextWrapper

import httpx
from PIL import Image, ImageDraw, ImageFont

from domain.assets.model import AssetType
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase, dataclass_to_dict
from domain.orders.repositories import OrderRepository
from domain.orders.services import CRM
from domain.previews import queries, errors, commands
from domain.previews.model import Preview, PreviewStatus
from domain.previews.repositories import PreviewRepository
from settings import SETTINGS


class StandardPreviewUseCase(UseCase, abc.ABC):
    def __init__(self, previews: PreviewRepository):
        super().__init__()
        self.previews = previews


class ApprovePreview(StandardPreviewUseCase):
    async def execute(self, query: queries.ApprovePreview) -> Preview:
        current_preview = await self.previews.get(query.preview_id)
        all_previews = await self.previews.get_by_order_id(current_preview.order_id)
        for preview in all_previews:
            await self.previews.disapprove_preview(preview.id)
        result = await self.previews.approve_preview(current_preview.id)
        return result


class CreatePreview(UseCase):
    def __init__(
        self,
        previews: PreviewRepository,
        assets: AssetRepository,
        crm: CRM,
        orders: OrderRepository,
    ):
        super().__init__()
        self.previews = previews
        self.assets = assets
        self.crm = crm
        self.orders = orders

    @staticmethod
    async def get_file_from_url(url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response

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
    async def async_open_file(response_content: bytes):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: Image.open(BytesIO(response_content))
        )

    @staticmethod
    async def fuse_images(cover_image_url, char_image_url, title, output_file_name):
        # Download the images
        cover_image_response = await CreatePreview.get_file_from_url(cover_image_url)
        char_image_response = await CreatePreview.get_file_from_url(char_image_url)

        # Open the images
        cover_image = await CreatePreview.async_open_file(cover_image_response.content)
        char_image = await CreatePreview.async_open_file(char_image_response.content)

        # First is width, second is height
        final_dimensions = (1312, 928)
        char_dimensions = (500, 750)

        # Resizing the dimensions of the images
        cover_image = cover_image.resize(final_dimensions)
        char_image = char_image.resize(char_dimensions)

        # Create a new blank image to hold the fused images
        fused_image = Image.new("RGBA", final_dimensions, (0, 0, 0, 0))

        # Paste the cover image onto the fused image at the top
        fused_image.paste(cover_image, (0, 0))

        # Create a mask for the character image
        char_mask = char_image.split()[3]  # Get the alpha channel
        char_image.putalpha(char_mask)

        # Adjust the alpha channel values to increase opacity
        char_alpha = char_image.getchannel("A")
        char_alpha = char_alpha.point(lambda x: 255 if x > 128 else x)

        # Update the alpha channel of the character image
        char_image.putalpha(char_alpha)

        char_position = (65, 928 - 750)

        fused_image.paste(
            char_image,
            char_position,
            mask=char_mask,
        )

        # Overlay the text onto the fused image
        draw = ImageDraw.Draw(fused_image)
        header_font_size = 60

        # URL to the font file on the CDN
        font_url = "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/fingerpaint.ttf"

        # Download the font file from the CDN
        font_response = await CreatePreview.get_file_from_url(font_url)
        font = ImageFont.truetype(BytesIO(font_response.content), header_font_size)

        wrapper = TextWrapper(width=33)
        wrapped_lines = wrapper.wrap(title)
        wrapped_title = "\n".join(line.center(33) for line in wrapped_lines)
        _, _, w, h = draw.textbbox((0, 0), wrapped_title, font=font)

        text_position = (2 * 152 * 4 - w, 2 * 23 * 4 - h / 2)

        text_shadow_response = await CreatePreview.get_file_from_url(
            "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/shadow_2.png"
        )
        text_shadow = await CreatePreview.async_open_file(text_shadow_response.content)

        text_shadow = text_shadow.resize(fused_image.size)
        shadow_mask = text_shadow.split()[3]

        fused_image.paste(
            text_shadow,
            (0, -50),
            mask=shadow_mask,
        )

        draw.text(
            text_position,
            wrapped_title,
            fill="white",
            font=font,
        )

        output_path = f"{SETTINGS.webserver.static_dir}/results/{output_file_name}.png"
        fused_image.save(output_path)
        return f"{SETTINGS.webserver.domain}/public/results/{output_file_name}.png"

    async def execute(self, cmd: commands.CreatePreview) -> Preview:
        asset_ids = cmd.asset_ids
        char_image_response = await self.assets.get(asset_id=cmd.asset_ids[2])
        char_image_url = char_image_response.value
        cover_image_response = await self.assets.get(asset_id=cmd.asset_ids[1])
        cover_image_url = cover_image_response.value
        title_response = await self.assets.get(asset_id=cmd.asset_ids[0])
        title = title_response.value
        result_url = await self.fuse_images(
            cover_image_url=cover_image_url,
            char_image_url=char_image_url,
            title=title,
            output_file_name=secrets.token_hex(6),
        )

        preview = Preview(
            asset_ids=asset_ids,
            order_id=cmd.order_id,
            status=PreviewStatus.COMPLETED,
            is_approved=False,
            title=title,
            character_image_url=char_image_url,
            cover_image_url=cover_image_url,
            fused_image_url=result_url,
        )

        await self.previews.add(preview)
        order = await self.orders.get(preview.order_id)
        await self.crm.update_deal(
            deal_id=order.deal_id, preview=json.dumps(dataclass_to_dict(preview))
        )
        return preview


class GetPreview(StandardPreviewUseCase):
    async def execute(self, query: queries.GetPreview) -> Preview:
        preview = await self.previews.get(query.preview_id)

        if preview is None:  # pragma: no cover
            raise errors.PreviewNotFound
        return preview


class GetPreviews(StandardPreviewUseCase):
    async def execute(self) -> list[Preview]:
        previews = await self.previews.list()
        return previews


class GetPreviewByOrderId(StandardPreviewUseCase):
    async def execute(self, query: queries.GetPreviewsByOrderId) -> list[Preview]:
        previews = await self.previews.get_by_order_id(query.order_id)

        return previews
