import secrets

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
        "name": "Tim",
        "city": "Hamburg",
        "birthday": "28/01/2019",
        "favourite_food": "Pizza",
        "interests": "Fussball",
        "event_to_come": "Urlaub in Spanien",
        "skin_tone": "fair",
        "hair_color": "blond",
        "hair_length": "short",
        "kids_photo": "string",
        "favourite_place": "Der Hamburger Hafen",
        "story_message": "Mut und Freundschaft überwinden alle Hindernisse",
        "personal_dedication": "Für dich meine Liebe",
        "age": "0-1",
        "gender": "girl",
        "hair_style": "straight",
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
            "title_prompt": "Standard Title",
        },
        "no_of_covers": 1,
    }
    response = client.post("/orders/", json=data)

    return Order.from_dict(response.json())


@pytest_asyncio.fixture
def preview(client, order):
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
