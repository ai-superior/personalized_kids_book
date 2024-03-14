import pytest


@pytest.mark.asyncio
async def test_get_contact(hubspot):
    contacts_response = await hubspot.get_contacts()
    result = contacts_response.json()
    assert len(result) >= 1


@pytest.mark.asyncio
async def test_get_contact(hubspot, contact):
    contact_response = await hubspot.get_contact(contact_id=contact["id"])
    assert contact_response.json()["id"] == contact["id"]


@pytest.mark.asyncio
async def test_get_deals(hubspot):
    contacts_response = await hubspot.get_deals()
    result = contacts_response.json()
    assert len(result) >= 1


@pytest.mark.asyncio
async def test_get_deal(hubspot, contact, deal):
    deal_response = await hubspot.get_deal(deal_id=deal["id"])
    assert deal_response.json()["id"] == deal["id"]


@pytest.mark.asyncio
async def test_update_assets(hubspot, deal):
    deal_response = await hubspot.update_deal(
        deal_id=deal["id"],
        assets="test_assets",
    )
    assert deal_response.status_code == 200


@pytest.mark.asyncio
async def test_update_preview(hubspot, deal):
    deal_response = await hubspot.update_deal(
        deal_id=deal["id"],
        preview="test_previews",
    )
    assert deal_response.status_code == 200
