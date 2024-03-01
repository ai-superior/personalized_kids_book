import secrets

import pytest
import pytest_asyncio

from domain.orders.model import Deal
from implementation.services.hubspot import Contact, HubSpot


def rand(num: int):
    return secrets.token_hex(num)


@pytest.fixture
def hubspot():
    return HubSpot()


@pytest_asyncio.fixture
async def contact(hubspot):
    random_contact = Contact(
        first_name=rand(3), last_name=rand(3), email=rand(5) + "@test.com"
    )
    contact_response = await hubspot.create_contact(contact=random_contact)
    return contact_response.json()


@pytest_asyncio.fixture
async def deal(hubspot, contact):
    random_deal = Deal(
        name=rand(3), contact_id=contact["id"], amount="30", stage="contractsent"
    )
    deal_response = await hubspot.create_deal(random_deal)
    return deal_response.json()
