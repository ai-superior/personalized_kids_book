import pytest


@pytest.mark.asyncio
async def test_seed_groups_creation(hubspot):
    groups_list = [
        ("kids_info", "Kids Info"),
        ("kids_info_aggregated", "Kids Info Aggregated"),
        ("wip", "Work In Progress"),
        ("order_and_preview_details", "Order And Preview Details"),
    ]
    for group in groups_list:
        await hubspot.create_group(group_name=group[0], group_label=group[1])
    #
    # for group in groups_list:
    #     await hubspot.delete_group(group_name=group[0])


@pytest.mark.asyncio
async def test_seed_property_creation(hubspot):
    properties_config = [
        {
            "kids_info": [
                "kids_name",
                "kids_gender",
                "kids_date_of_birth",
                "hair_color",
                "hair_length",
                "color_skin_tone",
                "city",
                "interest",
                "favourite_food",
                "upcoming_life_event",
                "intent_message",
                "story_location",
                "dedication",
            ]
        }
    ]
    for config in properties_config:
        for group, properties in config.items():
            for property_name in properties:
                await hubspot.create_text_property(
                    group_name=group, property_name=property_name
                )
    #
    # for config in properties_config:
    #     for group, properties in config.items():
    #         for property_name in properties:
    #             await hubspot.delete_property(property_name=property_name)
