import abc
import secrets
from io import BytesIO

import pandas as pd
import requests
from PIL import Image

from domain.assets import queries, errors, commands
from domain.assets.model import Asset, AssetType, AssetStatus
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase
from domain.orders.repositories import OrderRepository
from domain.orders.services import LLMProcessor
from settings import SETTINGS


class StandardAssetUseCase(UseCase, abc.ABC):
    def __init__(self, messages: AssetRepository):
        super().__init__()
        self.messages = messages


class CreateAsset(UseCase):
    def __init__(
        self, assets: AssetRepository, orders: OrderRepository, llm: LLMProcessor
    ):
        super().__init__()
        self.assets = assets
        self.llm = llm
        self.orders = orders

    @staticmethod
    def find_character(
        file_url, gender, age, hair_color, hair_length, hair_style, skin_tone
    ):
        file_response = requests.get(file_url)
        # Load the Excel file
        df = pd.read_excel(file_response.content, header=1)

        # Drop empty rows
        df.dropna(axis=0, how="all", inplace=True)

        # Remove redundant
        df = df[df["redundant"] != "x"]

        # Filter based on the criteria
        filtered_df = df[
            (df["gender"] == gender)
            & (df["age"] == age)
            & (df["hair color"] == hair_color)
            & (df["hair length"] == hair_length)
            & (df["hair style"] == hair_style)
            & (df["skin tone"] == skin_tone)
        ]

        # Check if there is a match
        first_result = "*missing"
        final_result = "*missing"

        if not filtered_df.empty:
            # Return the first matching Id
            first_result = filtered_df.iloc[0]["Id"]
        else:
            # No direct match found, implement logic for suggesting an alternative or return a default message
            return "*missing"

        if first_result == "*missing":
            final_result = filtered_df.iloc[0]["alternative character"]
        else:
            return f"https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/characters_imgs/{first_result}.png"

        return f"https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/characters_imgs/{final_result}.png"

    async def execute(self, cmd: commands.CreateAsset):
        assets = []

        title_prompt = requests.get(
            "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/book_title_template.txt"
        ).text
        cover_prompt = requests.get(
            "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/book_cover_template.txt"
        ).text

        order = self.orders.get(order_id=cmd.order_id)
        title_prompt = (
            title_prompt.replace("{{", "{")
            .replace("}}", "}")
            .format(
                name=order.name,
                city=order.city,
                birthday=order.birthday,
                favourite_food=order.favourite_food,
                interests=order.interests,
                favourite_place=order.favourite_place,
                event_to_come=order.event_to_come,
            )
        )

        titles_response = await self.llm.ask_for_text(
            prompt=title_prompt,
            quantity=cmd.no_of_covers,
        )
        titles = [title.message.content.strip('"') for title in titles_response.choices]

        char_url = self.find_character(
            file_url="https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/01_Character_excel.xlsx",
            gender=order.gender,
            age=order.age,
            hair_color=order.hair_color,
            hair_length=order.hair_length,
            hair_style=order.hair_style,
            skin_tone=order.skin_tone,
        )

        asset = Asset(
            order_id=cmd.order_id,
            type=AssetType.CHARACTER_IMAGE.value,
            status=AssetStatus.ACTIVE.value,
            value=char_url,
        )

        assets.append(asset)
        self.assets.add(asset)

        for i in range(cmd.no_of_covers):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE.value,
                status=AssetStatus.ACTIVE.value,
                prompt=title_prompt,
                value=titles[i],
            )
            assets.append(asset)
            self.assets.add(asset)

        print("cover_prompt: ", cover_prompt)
        cover_prompt = (
            cover_prompt.replace("{{", "{")
            .replace("}}", "}")
            .format(
                generated_title=titles[i],
            )
        )

        for i in range(cmd.no_of_covers):
            if i > 0:
                cover_prompt = cover_prompt.replace(titles[i - 1], titles[i])

            cover_image_gpt_response = await self.llm.ask_for_image(cover_prompt)

            cover_image_response = requests.get(cover_image_gpt_response.data[0].url)
            cover_image = Image.open(BytesIO(cover_image_response.content))
            output_file_name = secrets.token_hex(6)
            output_path = (
                f"{SETTINGS.webserver.static_dir}/results/{output_file_name}.png"
            )
            cover_image.save(output_path)
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.BACKGROUND_IMAGE.value,
                status=AssetStatus.ACTIVE.value,
                prompt=cover_prompt,
                value=f"{SETTINGS.webserver.domain}/public/results/{output_file_name}.png",
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


class GetAssets(StandardAssetUseCase):
    def execute(self) -> list[Asset]:
        assets = self.messages.list()
        return assets


class GetAssetByOrderId(StandardAssetUseCase):
    def execute(self, query: queries.GetAssetByOrderId) -> list[Asset]:
        assets = self.messages.get_by_order_id(query.order_id)

        if assets is None:  # pragma: no cover
            raise errors.AssetNotFound
        return assets
