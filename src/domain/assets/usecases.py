import abc
import asyncio
import json
import random
import re
import secrets
from io import BytesIO

import httpx
import pandas as pd
from PIL import Image

from domain.assets import queries, errors, commands
from domain.assets.model import Asset, AssetType, AssetStatus, AssetCategory
from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase, dataclass_to_dict
from domain.orders.model import LLMTextConfig, LLMImageConfig
from domain.orders.repositories import OrderRepository
from domain.orders.services import LLMProcessor, CRM
from settings import SETTINGS

stop_symbols = [
    "_",
    "-)",
    "=",
    "%",
    "}",
    ">",
    "<",
    "\\",
    "//",
    "~",
    "@",
    "어",
    "♀",
    "SQL",
    "条",
    "►",
    "[",
    "]",
    "코",
    "드",
    "함",
    "??",
    "!!",
    "..",
    "((",
    "))",
    "`",
    "#",
    "$",
    "^",
    "*",
    "►",
    " ,",
    ",)",
    "\n",
    "+",
]
stop_ending_words = [" and", " und", " FieldType"]


def find_dotted_letters(text):
    # The pattern matches a letter ([a-zA-Z]), followed by a dot (\.), followed by another letter ([a-zA-Z])
    pattern = r"[a-zA-Z]\.[a-zA-Z]"
    matches = re.findall(pattern, text)
    return matches


def remove_dot_at_end(s: str) -> str:
    # Check if the string ends with a dot and remove it if it does
    if s.endswith("."):
        return s[:-1]
    return s


def ends_with_word(s: str, words: list) -> bool:
    # Check if the string ends with any of the words in the list
    for word in words:
        if s.endswith(word):
            return True
    return False


def remove_quotes_if_both_ends(s: str) -> str:
    # Check if the string starts and ends with '"' and remove them if it does
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]  # Remove the leading and trailing '"'
    return s


def remove_bad_titles(titles, stop_symbols, stop_ending_words):
    resulting_titles = []
    bad_titles = []
    for title in titles:
        # Remove space at the end
        title = title.rstrip()

        # Remove " from start and end
        title = remove_quotes_if_both_ends(title)

        # Remove point at the end
        title = remove_dot_at_end(title)

        # check if the title end with a stop_word
        validation = ends_with_word(title, stop_ending_words)
        if validation:
            bad_titles.append(title)
            continue

        # check if the symbols are there
        validation = [symbol in title for symbol in stop_symbols]
        if sum(validation):
            bad_titles.append(title)
            continue

        # check if there is a dot between letters e.g. a.p - this is an indicator for bad title
        validation = find_dotted_letters(title)
        if len(validation):
            bad_titles.append(title)
            continue

        resulting_titles.append(title)

    return {"valid_titles": resulting_titles, "bad_titles": bad_titles}


class StandardAssetUseCase(UseCase, abc.ABC):
    def __init__(self, assets: AssetRepository):
        super().__init__()
        self.assets = assets


class CreateAsset(UseCase):
    def __init__(
        self,
        assets: AssetRepository,
        orders: OrderRepository,
        llm: LLMProcessor,
        crm: CRM,
    ):
        super().__init__()
        self.assets = assets
        self.llm = llm
        self.orders = orders
        self.crm = crm

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

        config_file_response = await CreateAsset.get_file_from_url(
            f"{SETTINGS.webserver.domain}/public/configs/config.json"
        )
        config_dict = config_file_response.json()

        selected_dict_titles = {}

        for key, values in config_dict.items():
            selected_dict_titles[key] = random.choice(values)

        order = await self.orders.get(order_id=cmd.order_id)
        title_prompt = (
            title_prompt.replace("{{", "{")
            .replace("}}", "}")
            .format(
                name=order.kids_name,
                city=order.city,
                birthday=order.kids_date_of_birth,
                favourite_food=order.favourite_food,
                interest=order.interest,
                upcoming_life_event=order.upcoming_life_event,
                story_location=order.story_location
                # story_location=selected_dict_titles["story_location"],
            )
        )

        title_configs = LLMTextConfig(
            model=cmd.additional_params.configs.title_configs.model,
            max_tokens=cmd.additional_params.configs.title_configs.max_tokens,
            temperature=cmd.additional_params.configs.title_configs.temperature,
            system_prompt=cmd.additional_params.configs.title_configs.system_prompt,
        )
        titles_response = await self.llm.ask_for_text(
            prompt=title_prompt,
            quantity=cmd.additional_params.total_no_of_titles,
            configs=title_configs,
        )
        titles = [
            title.message.content.strip().strip('"').strip("”")
            for title in titles_response.choices
        ]
        all_titles = remove_bad_titles(titles, stop_symbols, stop_ending_words)
        valid_titles = all_titles["valid_titles"][cmd.additional_params.no_of_covers :]
        valid_selectable_titles = all_titles["valid_titles"][
            : cmd.additional_params.no_of_covers
        ]
        bad_titles = all_titles["bad_titles"]

        char_url = await self.find_character(
            file_url="https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/01_Character_excel.xlsx",
            gender=order.kids_gender,
            age=order.age,
            hair_color=order.hair_color,
            hair_length=order.hair_length,
            skin_tone=order.color_skin_tone,
            hair_style="straight",
        )

        asset = Asset(
            order_id=cmd.order_id,
            type=AssetType.CHARACTER_IMAGE,
            status=AssetStatus.ACTIVE,
            value=char_url,
        )

        assets.append(asset)
        await self.assets.add(asset)

        for i in range(len(valid_titles)):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE,
                status=AssetStatus.ACTIVE,
                category=AssetCategory.VALID,
                prompt=title_prompt,
                value=valid_titles[i],
            )
            assets.append(asset)
            await self.assets.add(asset)

        for i in range(len(valid_selectable_titles)):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE,
                status=AssetStatus.ACTIVE,
                category=AssetCategory.SELECTABLE,
                prompt=title_prompt,
                value=valid_selectable_titles[i],
            )
            assets.append(asset)
            await self.assets.add(asset)

        for i in range(len(bad_titles)):
            asset = Asset(
                order_id=cmd.order_id,
                type=AssetType.TITLE,
                status=AssetStatus.ACTIVE,
                category=AssetCategory.BAD,
                prompt=title_prompt,
                value=bad_titles[i],
            )
            assets.append(asset)
            await self.assets.add(asset)

        initial_cover_prompt = cover_prompt

        for i in range(cmd.additional_params.no_of_covers):
            cover_prompt = initial_cover_prompt
            selected_dict = {}
            for key, values in config_dict.items():
                selected_dict[key] = random.choice(values)
                ## making sure that the random pool is from an unrepeated list
                if selected_dict[key].startswith("colors_type"):
                    config_dict[key].remove(selected_dict[key])

            cover_prompt = cover_prompt.format(**selected_dict)

            cover_prompt = (
                cover_prompt.replace("{{", "{")
                .replace("}}", "}")
                .format(
                    generated_title=valid_selectable_titles[0],
                    story_location=selected_dict_titles["story_location"],
                    animation_type=selected_dict["animation_type"],
                    colors_type=selected_dict["colors_type_" + str(i + 1)]
                    if (i + 1) <= 2
                    else selected_dict["colors_type_1"],
                    orientation=selected_dict["orientation"],
                )
            )

            if i > 0:
                cover_prompt = cover_prompt.replace(
                    valid_selectable_titles[i - 1], valid_selectable_titles[i]
                )

            cover_image_config = LLMImageConfig(
                model=cmd.additional_params.configs.cover_configs.model,
                quality=cmd.additional_params.configs.cover_configs.quality,
            )

            cover_image_gpt_response = await self.llm.ask_for_image(
                prompt=cover_prompt, configs=cover_image_config
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
                type=AssetType.BACKGROUND_IMAGE,
                status=AssetStatus.ACTIVE,
                prompt=cover_prompt,
                value=f"{SETTINGS.webserver.domain}/public/results/{output_file_name}.png",
                revised_cover_prompt=cover_image_gpt_response.data[0].revised_prompt,
            )

            assets.append(asset)
            await self.assets.add(asset)
            assets_json_list = []
            for asset in assets:
                assets_json_list.append(dataclass_to_dict(asset))

            await self.crm.update_deal(
                deal_id=order.deal_id, assets=json.dumps(assets_json_list)
            )

        return assets


class GetAssetByOrderId(UseCase):
    def __init__(self, assets: AssetRepository, crm: CRM, orders: OrderRepository):
        self.assets = assets
        self.crm = crm
        self.orders = orders

    async def execute(self, query: queries.GetAssetByOrderId) -> list[Asset]:
        order = await self.orders.get(query.order_id)
        assets = await self.assets.get_by_order_id(query.order_id)

        if assets[0].was_shown is not True:
            assets_json_list = []
            for asset in assets:
                assets_json_list.append(dataclass_to_dict(asset))

            await self.crm.update_deal(
                deal_id=order.deal_id, assets=json.dumps(assets_json_list)
            )

        if assets is None:  # pragma: no cover
            raise errors.AssetNotFound
        return assets


class GetAsset(StandardAssetUseCase):
    async def execute(self, query: queries.GetAsset) -> Asset:
        asset = await self.assets.get(query.asset_id)

        if asset is None:  # pragma: no cover
            raise errors.AssetNotFound
        return asset


class GetAssets(StandardAssetUseCase):
    async def execute(self) -> list[Asset]:
        assets = await self.assets.list()
        return assets
