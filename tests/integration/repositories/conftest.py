import secrets

import pytest

from dependencies import DependencyInjector
from domain.assets.model import Asset, AssetStatus, AssetType
from domain.orders.model import Order
from domain.previews.model import Preview, PreviewStatus


def random_name():
    return "integration-" + secrets.token_hex(4)


@pytest.fixture
def order():
    random_lead = Order(
        email=f"{secrets.token_hex(5)}@example.com",
        name=secrets.token_hex(5),
        city=secrets.token_hex(5),
        birthday=secrets.token_hex(5),
        favourite_food=secrets.token_hex(5),
        interests=secrets.token_hex(5),
        event_to_come=secrets.token_hex(5),
        skin_tone=secrets.token_hex(5),
        hair_color=secrets.token_hex(5),
        hair_length=secrets.token_hex(5),
        kids_photo=f"path/to/photos/{secrets.token_hex(5)}.jpg",
        favourite_place=secrets.token_hex(5),
        story_message=secrets.token_hex(5),
        personal_dedication=secrets.token_hex(5),
        gender=secrets.token_hex(5),
        age=secrets.token_hex(5),
        hair_style=secrets.token_hex(5),
    )
    DependencyInjector.get().orders().add(random_lead)
    return random_lead


@pytest.fixture
def asset():
    random_asset = Asset(
        order_id=secrets.token_hex(5),
        status=AssetStatus.PENDING.value,
        type=AssetType.TITLE.value,
    )
    DependencyInjector.get().assets().add(random_asset)
    return random_asset


@pytest.fixture()
def preview():
    random_preview = Preview(
        asset_ids=[secrets.token_hex(5)],
        status=PreviewStatus.PENDING.value,
        is_approved=False,
        order_id=secrets.token_hex(5),
        title="str",
        cover_image_url="str",
        fused_image_url="str",
    )
    DependencyInjector.get().previews().add(random_preview)
    return random_preview
