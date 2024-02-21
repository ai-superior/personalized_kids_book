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
            "cover_prompt": "\n# Generate a scenery Cover for a children book in a 3D pixar cartoon style. Here is a title that describes the story:\n\nTitle: {{generated_title}}\n\n# Additional notes:\n1. Image orientation: horizontal\n2. Important: Ensure the image is free from any textual elements.\n3. Important: It is only background, without people or animals or any other characters on the image.\n",
            "title_prompt": "\nAct as a creative German book author. Create a title for the children book story.\n\nTitle should adhere to following rules:\n1. Language - German\n2. Included Child's name\n3. Word-playful and engaging \n4. Title should be based on following information about the child:\n\nChild's information below:\nName is {{name}}\nCity is {{city}}\nBirthday is {{birthday}}\nFavorite food is {{favourite_food}}\nInterests are {{interests}}\nFavorite place is {{favourite_place}}\nAn expected event is {{event_to_come}}\n\n\nHere are Examples of the book titles with desired format and suitable presentation of result:\na. Mutige Alma und die Osterferien auf dem Pferdehof\nb. Alma, die Weißwurstprinzessin und das Turnier der musikalischen Freunde\nc. Alma, die Weißwurst-Detektivin und das Geheimnis der verschwundenen Osterhasen\n\n\nThe title length must not be more than 10 words.\n",
        },
        "no_of_covers": 1,
    }
    response = client.post("/orders/", json=data)
    return Order.from_dict(response.json())


@pytest.fixture
def assets(client, order):
    data = {"order_id": order.id, "no_of_covers": 3}
    response = client.post("/assets", json=data)
    assets = [Asset.from_dict(asset) for asset in response.json()]
    return assets


@pytest.fixture
def preview(client, order, assets):
    data = {
        "order_id": order.id,
        "asset_ids": [
            [asset.id for asset in assets if asset.type == "TITLE"][0],
            [asset.id for asset in assets if asset.type == "BACKGROUND_IMAGE"][0],
            [asset.id for asset in assets if asset.type == "CHARACTER_IMAGE"][0],
        ],
    }

    response = client.post("/previews", json=data)
    return Preview.from_dict(response.json())
