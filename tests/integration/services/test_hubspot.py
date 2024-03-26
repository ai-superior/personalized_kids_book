import pytest


@pytest.mark.asyncio
async def test_get_contact(hubspot):
    contacts_response = await hubspot.get_contacts()
    result = contacts_response.json()
    assert len(result) >= 1


@pytest.mark.asyncio
async def test_get_contact(hubspot, contact: dict):
    contact_response = await hubspot.get_contact(contact_id=contact["id"])
    assert contact_response.json()["id"] == contact["id"]


@pytest.mark.asyncio
async def test_get_deals(hubspot):
    contacts_response = await hubspot.get_deals()
    result = contacts_response.json()
    assert len(result) >= 1


@pytest.mark.asyncio
async def test_get_deal(hubspot, contact, deal: dict):
    deal_response = await hubspot.get_deal(deal_id=deal["id"])
    assert deal_response.json()["id"] == deal["id"]


@pytest.mark.asyncio
async def test_update_assets(hubspot, deal: dict):
    deal_response = await hubspot.update_deal(
        deal_id=deal["id"],
        assets="test_assets",
    )
    assert deal_response.status_code == 200


@pytest.mark.asyncio
async def test_update_preview(hubspot, deal: dict):
    deal_response = await hubspot.update_deal(
        deal_id=deal["id"],
        preview="test_previews",
    )
    assert deal_response.status_code == 200


@pytest.mark.asyncio
async def test_create_delete_group(hubspot):
    created_group_response = await hubspot.create_group(
        group_name="kids_info", group_label="Kids Info"
    )
    assert created_group_response.status_code == 201
    deleted_group_response = await hubspot.delete_group("kids_info")
    assert deleted_group_response.status_code == 204


@pytest.mark.asyncio
async def test_create_text_property(hubspot):
    created_group_response = await hubspot.create_group(
        group_name="kids_info", group_label="Kids Info"
    )
    assert created_group_response.status_code == 201
    created_property_response = await hubspot.create_text_property(
        group_name="kids_info", property_name="kids_name"
    )
    assert created_property_response.status_code == 201
    deleted_property_response = await hubspot.delete_property(property_name="kids_name")
    assert deleted_property_response.status_code == 204
    await hubspot.delete_group("kids_info")


@pytest.mark.asyncio
async def test_create_dropdown_property(hubspot):
    await hubspot.create_group(group_name="kids_info", group_label="Kids Info")
    created_property_response = await hubspot.create_dropdown_property(
        group_name="kids_info",
        property_name="test_dd",
        possible_values=["option1", "option2"],
    )
    assert created_property_response.status_code == 201
    await hubspot.delete_property(property_name="test_dd")
    await hubspot.delete_group(group_name="kids_info")
