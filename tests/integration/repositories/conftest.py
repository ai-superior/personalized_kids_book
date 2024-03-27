import secrets

import pytest_asyncio

from dependencies import DependencyInjector
from domain.assets.model import Asset, AssetStatus, AssetType
from domain.orders.model import Order, Configs, CoverConfigs, TitleConfigs, Prompt
from domain.previews.model import Preview, PreviewStatus


def random_name():
    return "integration-" + secrets.token_hex(4)


@pytest_asyncio.fixture
async def order():
    random_order = Order(
        email=f"{secrets.token_hex(5)}@example.com",
        kids_name=secrets.token_hex(5),
        city=secrets.token_hex(5),
        kids_date_of_birth=secrets.token_hex(5),
        favourite_food=secrets.token_hex(5),
        interest=secrets.token_hex(5),
        upcoming_life_event=secrets.token_hex(5),
        color_skin_tone=secrets.token_hex(5),
        hair_color=secrets.token_hex(5),
        hair_length=secrets.token_hex(5),
        image=f"path/to/photos/{secrets.token_hex(5)}.jpg",
        favourite_place=secrets.token_hex(5),
        story_message=secrets.token_hex(5),
        personal_dedication=secrets.token_hex(5),
        kids_gender=secrets.token_hex(5),
        age=secrets.token_hex(5),
        hair_style=secrets.token_hex(5),
        no_of_covers=2,
        configs=Configs(
            cover_configs=CoverConfigs(quality="standard", model="dall-e-3"),
            title_configs=TitleConfigs(
                temperature=1.7,
                max_tokens=150,
                model="gpt-4-1106-preview",
                system_prompt="you are helpful assistant",
            ),
        ),
        prompts=Prompt(cover_prompt="test", title_prompt="test"),
    )
    await DependencyInjector.get().orders().add(random_order)
    return random_order


@pytest_asyncio.fixture
async def asset():
    random_asset = Asset(
        order_id=secrets.token_hex(5),
        status=AssetStatus.PENDING,
        type=AssetType.TITLE,
    )
    await DependencyInjector.get().assets().add(random_asset)
    return random_asset


@pytest_asyncio.fixture()
async def preview():
    random_preview = Preview(
        asset_ids=[secrets.token_hex(5)],
        status=PreviewStatus.PENDING,
        is_approved=False,
        order_id=secrets.token_hex(5),
        title="str",
        cover_image_url="str",
        fused_image_url="str",
    )
    await DependencyInjector.get().previews().add(random_preview)
    return random_preview
