import secrets

import pytest

from dependencies import DependencyInjector
from domain.leads.model import Lead


def random_name():
    return "integration-" + secrets.token_hex(4)


@pytest.fixture
def lead():
    random_lead = Lead(
        email=f"{secrets.token_hex(5)}@example.com",
        name=secrets.token_hex(5),
        city=secrets.token_hex(5),
        birthday=secrets.token_hex(5),
        favourite_food=secrets.token_hex(5),
        likes=secrets.token_hex(5),
        activities=secrets.token_hex(5),
        skin_tone=secrets.token_hex(5),
        hair_color=secrets.token_hex(5),
        hair_length=secrets.token_hex(5),
        kids_photo=f"path/to/photos/{secrets.token_hex(5)}.jpg",
    )
    DependencyInjector.get().leads().add(random_lead)
    return random_lead
