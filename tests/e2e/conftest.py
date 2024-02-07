import secrets

import pytest
from starlette.testclient import TestClient

from dependencies import DependencyInjector
from domain.orders.model import Order
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
        "email": random_name(5),
        "name": random_name(5),
        "city": random_name(5),
        "birthday": random_name(5),
        "favourite_food": random_name(5),
        "interests": random_name(5),
        "event_to_come": random_name(5),
        "skin_tone": random_name(5),
        "hair_color": random_name(5),
        "hair_length": random_name(5),
        "kids_photo": random_name(5),
        "favourite_place": random_name(5),
        "story_message": random_name(5),
        "personal_dedication": random_name(5),
    }
    response = client.post("/orders/", json=data)
    return Order.from_dict(response.json())
