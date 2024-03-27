import secrets
from time import sleep

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from dependencies import DependencyInjector
from domain.orders.model import Order
from domain.previews.model import Preview
from main import create_fastapi_app

di = DependencyInjector.get()


def random_name(len_chars):
    return "e2e-tests-" + secrets.token_hex(len_chars)


@pytest.fixture
def client():
    app = create_fastapi_app()
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def order(client):
    data = {
        "email": "someemail@gmail.com",
        "kids_name": "Tim",
        "kids_gender": "girl",
        "hair_color": "blond",
        "hair_length": "short",
        "color_skin_tone": "fair",
        "no_of_covers": 1,
        "configs": {
            "cover_configs": {"quality": "standard", "model": "dall-e-3"},
            "title_configs": {
                "temperature": 1.7,
                "max_tokens": 150,
                "model": "gpt-4-1106-preview",
                "system_prompt": "You are a helpful assistant",
            },
        },
        "prompts": {
            "cover_prompt": "Standard Image",
            "title_prompt": "Just return a title in 4 words",
        },
    }
    response = client.post("/orders/", json=data)

    return Order.from_dict(response.json())


@pytest_asyncio.fixture
def preview(client, order):
    assets_status_flag = False
    while not assets_status_flag:
        assets_status_flag = client.get(f"/orders/order_status/{order.id}").json()
        sleep(10)
    assets_response = client.get(f"/assets/order_id/{order.id}")
    assets = assets_response.json()
    data = {
        "order_id": order.id,
        "asset_ids": [
            [asset["id"] for asset in assets if asset["type"] == "TITLE"][0],
            [asset["id"] for asset in assets if asset["type"] == "BACKGROUND_IMAGE"][0],
            [asset["id"] for asset in assets if asset["type"] == "CHARACTER_IMAGE"][0],
        ],
    }

    response = client.post("/previews", json=data)
    return Preview.from_dict(response.json())
