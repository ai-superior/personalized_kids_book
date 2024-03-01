import abc
import asyncio
import secrets
from io import BytesIO
from textwrap import TextWrapper

import httpx
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

    async def fuse_images(
        self, cover_image_url, char_image_url, title, output_file_name
    ):
        # Download the images
        cover_image_response = await self.get_file_from_url(cover_image_url)
        char_image_response = await self.get_file_from_url(char_image_url)

        # Open the images
        cover_image = await self.async_open_file(cover_image_response.content)
        char_image = await self.async_open_file(char_image_response.content)

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
        font_response = await self.get_file_from_url(font_url)
        font = ImageFont.truetype(BytesIO(font_response.content), header_font_size)

        wrapper = TextWrapper(width=33)
        wrapped_lines = wrapper.wrap(title)
        wrapped_title = "\n".join(line.center(33) for line in wrapped_lines)

        # wrapped_title = wrapper.fill(title)

        _, _, w, h = draw.textbbox((0, 0), wrapped_title, font=font)

        text_position = (2 * 152 * 4 - w, 2 * 23 * 4 - h / 2)

        # outline_color = "white"
        # outline_thickness = 2
        #
        # for dx in [-outline_thickness, 0, outline_thickness]:
        #     for dy in [-outline_thickness, 0, outline_thickness]:
        #         draw.text(
        #             (text_position[0] + dx, text_position[1] + dy),
        #             wrapped_title,
        #             font=font,
        #             fill=outline_color,
        #         )
        text_mask = Image.new("L", fused_image.size, 0)
        draw_mask = ImageDraw.Draw(text_mask)
        draw_mask.text(text_position, wrapped_title, fill=255, font=font)
        shadow_mask = text_mask.filter(ImageFilter.GaussianBlur(radius=10))
        shadow_mask = shadow_mask.point(lambda p: p * 1.2)
        shadow_color = (
            0,
            0,
            0,
            100,
        )
        shadow_image = Image.new("RGBA", fused_image.size, shadow_color)

        # Ensure the alpha channel around the text is black
        shadow_image.putalpha(text_mask)

        # Paste the shadow image onto the fused image using the shadow mask
        fused_image.paste(shadow_image, (0, 0), mask=shadow_mask)

        draw.text(
            text_position,
            wrapped_title,
            fill="white",
            font=font,
        )

        # Save the fused image
        output_path = f"{SETTINGS.webserver.static_dir}/results/{output_file_name}.png"
        fused_image.save(output_path)
        return f"{SETTINGS.webserver.domain}/public/results/{output_file_name}.png"

    def __init__(self, previews: PreviewRepository, assets: AssetRepository):
        super().__init__()
        self.previews = previews
        self.assets = assets

    async def execute(self, cmd: commands.CreatePreview) -> Preview:
        asset_ids = cmd.asset_ids
        char_image_response = await self.assets.get(cmd.asset_ids[2])
        char_image_url = char_image_response.value
        cover_image_response = await self.assets.get(cmd.asset_ids[1])
        cover_image_url = cover_image_response.value
        title_response = await self.assets.get(cmd.asset_ids[0])
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
            status=PreviewStatus.COMPLETED.value,
            is_approved=False,
            title=title,
            character_image_url=char_image_url,
            cover_image_url=cover_image_url,
            fused_image_url=result_url,
        )

        await self.previews.add(preview)
        return preview


class GetPreview(StandardPreviewUseCase):
    async def execute(self, query: queries.GetPreview) -> Preview:
        preview = await self.messages.get(query.preview_id)

        if preview is None:  # pragma: no cover
            raise errors.PreviewNotFound
        return preview


class GetPreviews(StandardPreviewUseCase):
    async def execute(self) -> list[Preview]:
        previews = await self.messages.list()
        return previews


class GetPreviewByOrderId(StandardPreviewUseCase):
    async def execute(self, query: queries.GetPreviewsByOrderId) -> list[Preview]:
        previews = await self.messages.get_by_order_id(query.order_id)

        return previews
