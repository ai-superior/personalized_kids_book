import secrets

import pytest
from starlette.testclient import TestClient

from dependencies import DependencyInjector
from domain.assets.model import Asset
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
        "skin_tone": "Hell",
        "hair_color": "Blond",
        "hair_length": "Kurz",
        "kids_photo": "string",
        "favourite_place": "Der Hamburger Hafen",
        "story_message": "Mut und Freundschaft überwinden alle Hindernisse",
        "personal_dedication": "Für dich meine Liebe",
    }
    response = client.post("/orders/", json=data)
    return Order.from_dict(response.json())


@pytest.fixture
def assets(client, order):
    data = {"order_id": order.id, "no_of_titles": 1, "no_of_cover_images": 1}
    response = client.post("/assets", json=data)
    assets = [Asset.from_dict(asset) for asset in response.json()]
    return assets


@pytest.fixture
def preview(client, order, assets):
    data = {"order_id": order.id, "asset_ids": [asset.id for asset in assets]}
    response = client.post("/previews", json=data)
    return Preview.from_dict(response.json())
