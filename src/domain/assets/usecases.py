import abc

import requests

from domain.assets import queries, errors, commands
from domain.assets.model import Asset, AssetType, AssetStatus
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase
from domain.orders.services import LLMProcessor


class StandardAssetUseCase(UseCase, abc.ABC):
    def __init__(self, messages: AssetRepository):
        super().__init__()
        self.messages = messages


class CreateAsset(UseCase):
    def __init__(self, assets: AssetRepository, llm: LLMProcessor):
        super().__init__()
        self.assets = assets
        self.llm = llm

    async def execute(self, cmd: commands.CreateAsset):
        assets = []

        title_prompt = requests.get(
            "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/book_title_template.txt"
        ).text
        cover_prompt = requests.get(
            "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/book_cover_template.txt"
        ).text
        titles_response = await self.llm.ask_for_text(
            prompt=title_prompt,
            # "Generate a standard Book Title. Just the title and nothing else",
            quantity=cmd.no_of_titles,
        )
        titles = [title.message.content for title in titles_response.choices]

        for i in range(cmd.no_of_titles):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE.value,
                status=AssetStatus.ACTIVE.value,
                value=titles[i],
            )
            assets.append(asset)
            self.assets.add(asset)

        for i in range(cmd.no_of_cover_images):
            cover_images_response = await self.llm.ask_for_image(
                cover_prompt
                # "Generate standard cover for a book"
            )
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.BACKGROUND_IMAGE.value,
                status=AssetStatus.ACTIVE.value,
                value=cover_images_response.data[0].url,
            )
            assets.append(asset)
            self.assets.add(asset)

        asset = Asset(
            order_id=cmd.order_id,
            type=AssetType.CHARACTER_IMAGE.value,
            status=AssetStatus.ACTIVE.value,
            value="https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/mock_character.jpg",
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
