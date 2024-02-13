import abc

import requests

from domain.assets import queries, errors, commands
from domain.assets.model import Asset, AssetType, AssetStatus
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase
from domain.orders.repositories import OrderRepository
from domain.orders.services import LLMProcessor


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
        titles = [title.message.content for title in titles_response.choices]

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

        for i in range(cmd.no_of_covers):
            cover_prompt = (
                cover_prompt.replace("{{", "{")
                .replace("}}", "}")
                .format(
                    generated_title=titles[i],
                )
            )

            cover_images_response = await self.llm.ask_for_image(cover_prompt)
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.BACKGROUND_IMAGE.value,
                status=AssetStatus.ACTIVE.value,
                prompt=cover_prompt,
                value=cover_images_response.data[0].url,
            )
            assets.append(asset)
            self.assets.add(asset)

        asset = Asset(
            order_id=cmd.order_id,
            type=AssetType.CHARACTER_IMAGE.value,
            status=AssetStatus.ACTIVE.value,
            value="https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/test_2_char.png",
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
