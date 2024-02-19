import abc
import secrets
from io import BytesIO
from textwrap import TextWrapper

import requests
from PIL import Image, ImageDraw, ImageFont

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
        cover_image_response = requests.get(cover_image_url)
        char_image_response = requests.get(char_image_url)

        # Open the images
        cover_image = Image.open(BytesIO(cover_image_response.content))
        char_image = Image.open(BytesIO(char_image_response.content))

        # First is width, second is height
        final_dimensions = (1312, 928)
        # final_dimensions = cover_image.size
        char_dimensions = char_image.size

        # Resizing the dimensions of the images
        cover_image = cover_image.resize(final_dimensions)
        # char_image = char_image.resize(char_dimensions)

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

        # Paste the character image onto the fused image at the calculated position
        # fused_image.paste(
        #     char_image, (-30, final_dimensions[1] - char_image.size[1]), mask=char_mask
        # )
        char_position = (2 * 65, 928 - 560)
        # char_position = (
        #     2 * 65 * 4 - char_dimensions[0],
        #     2 * 140 * 4 - char_dimensions[1],
        # )
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
        font_response = requests.get(font_url)
        font = ImageFont.truetype(BytesIO(font_response.content), header_font_size)

        wrapper = TextWrapper(width=33)
        wrapped_lines = wrapper.wrap(title)
        wrapped_title = "\n".join(line.center(33) for line in wrapped_lines)

        # wrapped_title = wrapper.fill(title)

        _, _, w, h = draw.textbbox((0, 0), wrapped_title, font=font)

        text_position = (2 * 152 * 4 - w, 2 * 23 * 4 - h / 2)

        # text_position = (2 * 152 * 4 - w, 2 * 23 * 4 - h / 2)

        outline_color = "black"
        outline_thickness = 2

        for dx in [-outline_thickness, 0, outline_thickness]:
            for dy in [-outline_thickness, 0, outline_thickness]:
                draw.text(
                    (text_position[0] + dx, text_position[1] + dy),
                    wrapped_title,
                    font=font,
                    fill=outline_color,
                )

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

    def execute(self, cmd: commands.CreatePreview) -> Preview:
        # assets = self.assets.get_by_order_id(cmd.order_id)

        # assets_for_preview = self.assets_for_preview(assets)
        # assets_for_preview = assets

        # if cmd.asset_ids is None:
        #     assets_for_preview = [asset.id for asset in assets_for_preview]
        # else:
        #     assets_for_preview = cmd.asset_ids

        # asset_ids = [asset.id for asset in assets_for_preview]
        asset_ids = cmd.asset_ids
        char_image_url = self.assets.get(cmd.asset_ids[2]).value
        cover_image_url = self.assets.get(cmd.asset_ids[1]).value
        title = self.assets.get(cmd.asset_ids[0]).value
        result_url = self.fuse_images(
            cover_image_url, char_image_url, title, secrets.token_hex(6)
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

        self.previews.add(preview)
        return preview


class GetPreview(StandardPreviewUseCase):
    def execute(self, query: queries.GetPreview) -> Preview:
        preview = self.messages.get(query.preview_id)

        if preview is None:  # pragma: no cover
            raise errors.PreviewNotFound
        return preview


class GetPreviews(StandardPreviewUseCase):
    def execute(self) -> list[Preview]:
        previews = self.messages.list()
        return previews


class GetPreviewByOrderId(StandardPreviewUseCase):
    def execute(self, query: queries.GetPreviewsByOrderId) -> list[Preview]:
        previews = self.messages.get_by_order_id(query.order_id)

        return previews
