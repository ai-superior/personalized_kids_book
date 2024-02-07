import secrets

import pytest

from dependencies import DependencyInjector
from domain.orders.model import Order


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
    )
    DependencyInjector.get().orders().add(random_lead)
    return random_lead
