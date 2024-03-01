import abc
import asyncio
import secrets
from io import BytesIO

import httpx
import pandas as pd
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
    async def get_file_from_url(url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response

    @staticmethod
    async def read_excel_async(file_content):
        return await asyncio.to_thread(pd.read_excel, BytesIO(file_content), header=1)

    @staticmethod
    async def async_open_image(response_content: bytes):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: Image.open(BytesIO(response_content))
        )

    async def find_character(
        self, file_url, gender, age, hair_color, hair_length, hair_style, skin_tone
    ):
        file_response = await self.get_file_from_url(file_url)
        # Load the Excel file
        df = await self.read_excel_async(file_response.content)

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
            return "*missing"

        if first_result == "*missing":
            final_result = filtered_df.iloc[0]["alternative character"]
        else:
            return f"https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/characters_imgs/{first_result}.png"

        return f"https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/characters_imgs/{final_result}.png"

    async def execute(self, cmd: commands.CreateAsset):
        assets = []

        title_prompt = cmd.additional_params.prompts.title_prompt
        cover_prompt = cmd.additional_params.prompts.cover_prompt

        order = await self.orders.get(order_id=cmd.order_id)
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
            quantity=cmd.additional_params.no_of_covers,
            configs=cmd.additional_params,
        )
        titles = [
            title.message.content.strip('"').strip("”")
            for title in titles_response.choices
        ]

        char_url = await self.find_character(
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
        await self.assets.add(asset)

        for i in range(cmd.additional_params.no_of_covers):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE.value,
                status=AssetStatus.ACTIVE.value,
                prompt=title_prompt,
                value=titles[i],
            )
            assets.append(asset)
            await self.assets.add(asset)

        cover_prompt = (
            cover_prompt.replace("{{", "{")
            .replace("}}", "}")
            .format(
                generated_title=titles[0],
            )
        )

        for i in range(cmd.additional_params.no_of_covers):
            if i > 0:
                cover_prompt = cover_prompt.replace(titles[i - 1], titles[i])

            cover_image_gpt_response = await self.llm.ask_for_image(
                prompt=cover_prompt, configs=cmd.additional_params
            )

            cover_image_response = await self.get_file_from_url(
                cover_image_gpt_response.data[0].url
            )
            cover_image = await self.async_open_image(cover_image_response.content)
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
            await self.assets.add(asset)

        return assets


class GetAsset(StandardAssetUseCase):
    async def execute(self, query: queries.GetAsset) -> Asset:
        asset = await self.messages.get(query.asset_id)

        if asset is None:  # pragma: no cover
            raise errors.AssetNotFound
        return asset


class GetAssets(StandardAssetUseCase):
    async def execute(self) -> list[Asset]:
        assets = await self.messages.list()
        return assets


class GetAssetByOrderId(StandardAssetUseCase):
    async def execute(self, query: queries.GetAssetByOrderId) -> list[Asset]:
        assets = await self.messages.get_by_order_id(query.order_id)

        if assets is None:  # pragma: no cover
            raise errors.AssetNotFound
        return assets
