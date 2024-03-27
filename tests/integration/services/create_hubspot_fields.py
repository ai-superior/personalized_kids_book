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

    # for group in groups_list:
    #     await hubspot.delete_group(group_name=group[0])


@pytest.mark.asyncio
async def test_seed_text_property_creation(hubspot):
    properties_config = [
        {
            "kids_info": [
                {"kids_name": ("text", "string")},
                {"kids_gender": ["male", "female"]},
                {"kids_date_of_birth": ("text", "string")},
                {
                    "hair_color": [
                        "blond",
                        "black",
                    ]
                },
                {"hair_length": ["short", "long"]},
                {"color_skin_tone": ["fair", "dark"]},
                {"city": ("text", "string")},
                {"interest": ("text", "string")},
                {"favourite_food": ("text", "string")},
                {"upcoming_life_event": ["birthday", "vacation"]},
                {"intent_message": ("text", "string")},
                {
                    "story_location": [
                        "German Village",
                        "Magical Forest",
                        "Beach Coast",
                        "Flower Garden",
                        "Moon",
                        "Jungle",
                        "Magical Playground",
                        "Dinosaur World",
                    ]
                },
                {"mood": ["happy", "fun"]},
                {"dedication": ("textarea", "string")},
            ],
            "kids_info_aggregated": [
                {"child_info_for_story_creation": ("textarea", "string")},
                {"dedication": ("textarea", "string")},
                {"child_visuals_for_character_creation": ("textarea", "string")},
            ],
            "wip": [
                {
                    "preview_url": ("text", "string"),
                    "character_id": ("text", "string"),
                    "title": ("text", "string"),
                    "story_outline": ("text", "string"),
                    "stotry_prompt_ready": ("text", "string"),
                    "generated_story": ("text", "string"),
                    "generated_story_en": ("text", "string"),
                    "scenery_images_prompts": ("text", "string"),
                    "cover_prompt": ("text", "string"),
                    "title_prompt": ("text", "string"),
                }
            ],
            "order_and_preview_details": [
                {
                    "order_started": ["True", "False"],
                    "order_submitted": ["True", "False"],
                    "order_id": ("text", "string"),
                    "order_json": ("textarea", "string"),
                    "asset_json": ("textarea", "string"),
                    "preview_json": ("textarea", "string"),
                    "assets_generated": ["True", "False"],
                    "assets_shown": ["True", "False"],
                    "preview_generated": ["True", "False"],
                    "preview_shown": ["True", "False"],
                    "preview_approved": ["True", "False"],
                }
            ],
        }
    ]
    for config in properties_config:
        for group_name, properties_list in config.items():
            for property_dict in properties_list:
                for property_name, possible_values in property_dict.items():
                    if isinstance(possible_values, tuple):
                        response = await hubspot.create_property(
                            group_name=group_name,
                            property_name=property_name,
                            field_type=possible_values[0],
                            data_type=possible_values[1],
                        )
                    elif isinstance(possible_values, list):
                        await hubspot.create_dropdown_property(
                            group_name=group_name,
                            property_name=property_name,
                            possible_values=possible_values,
                        )

    # for config in properties_config:
    #     for group, properties_list in config.items():
    #         for property_dict in properties_list:
    #             for property_name, types in property_dict.items():
    #                 await hubspot.delete_property(property_name=property_name)
