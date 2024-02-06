import abc
from io import BytesIO
from uuid import uuid4

import requests
from PIL import Image, ImageDraw, ImageFont

from domain.basic_types import UseCase
from domain.orders import queries, errors, commands, model
from domain.orders.model import Order
from domain.orders.repositories import OrderRepository
from domain.orders.services import LLMProcessor


def character_generator():
    return "https://pkb-assets.s3.eu-central-1.amazonaws.com/mock_character.jpg"


def fuse_images(image_url1, image_url2, text, output_file_name):
    # Download the images
    response1 = requests.get(image_url1)
    response2 = requests.get(image_url2)

    # Open the images
    image1 = Image.open(BytesIO(response1.content))
    image2 = Image.open(BytesIO(response2.content))

    # Resize the images to the same dimensions
    image1 = image1.resize(image2.size)

    # Overlay the text onto the first image
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(
        "assets/arial.ttf", 30
    )  # Change the font and size as needed
    draw.text((10, 10), text, font=font, fill="red")

    # Blend the images together
    fused_image = Image.blend(image1, image2, alpha=0.5)

    fused_image.save(f"public/results/{output_file_name}.jpg")

    # Return the fused image
    return f"http://0.0.0.0:8000/public/results/{output_file_name}.jpg"


class StandardOrderUseCase(UseCase, abc.ABC):
    def __init__(self, messages: OrderRepository):
        super().__init__()
        self.messages = messages


class CreateOrder(UseCase):
    def __init__(self, orders: OrderRepository, llm: LLMProcessor):
        super().__init__()
        self.orders = orders
        self.llm = llm

    async def execute(self, cmd: commands.CreateOrders):
        with open("src/config/book_title_template.txt") as f:
            book_cover_template = f.read()
            title_prompt = (
                book_cover_template.replace("{{", "{")
                .replace("}}", "}")
                .format(
                    name=cmd.name,
                    city=cmd.city,
                    birthday=cmd.birthday,
                    favourite_food=cmd.favourite_food,
                    interests=cmd.interests,
                    event_to_come=cmd.event_to_come,
                    skin_tone=cmd.skin_tone,
                    hair_color=cmd.hair_color,
                    hair_length=cmd.hair_length,
                    kids_photo=cmd.kids_photo,
                    favourite_place=cmd.favourite_place,
                    story_message=cmd.story_message,
                    personal_dedication=cmd.personal_dedication,
                )
            )

        with open("src/config/book_cover_template.txt") as f:
            book_cover_template = f.read()
            book_cover_prompt = (
                book_cover_template.replace("{{", "{")
                .replace("}}", "}")
                .format(
                    name=cmd.name,
                    city=cmd.city,
                    birthday=cmd.birthday,
                    favourite_food=cmd.favourite_food,
                    interests=cmd.interests,
                    event_to_come=cmd.event_to_come,
                    skin_tone=cmd.skin_tone,
                    hair_color=cmd.hair_color,
                    hair_length=cmd.hair_length,
                    kids_photo=cmd.kids_photo,
                    favourite_place=cmd.favourite_place,
                    story_message=cmd.story_message,
                    personal_dedication=cmd.personal_dedication,
                )
            )

        title_response = await self.llm.ask_for_text(prompt=title_prompt)
        book_cover_response = await self.llm.ask_for_image(prompt=book_cover_prompt)

        output_file_name = str(uuid4())

        final_result_url = fuse_images(
            text=title_response.choices[0].message.content,
            image_url1=book_cover_response.data[0].url,
            image_url2=character_generator(),
            output_file_name=output_file_name,
        )

        result = model.Result(
            title=title_response.choices[0].message.content,
            cover_url=book_cover_response.data[0].url,
            character_url=character_generator(),
            final_result_url=final_result_url,
        )

        order = model.Order(
            email=cmd.email,
            name=cmd.name,
            city=cmd.city,
            birthday=cmd.birthday,
            favourite_food=cmd.favourite_food,
            interests=cmd.interests,
            event_to_come=cmd.event_to_come,
            skin_tone=cmd.skin_tone,
            hair_color=cmd.hair_color,
            hair_length=cmd.hair_length,
            kids_photo=cmd.kids_photo,
            favourite_place=cmd.favourite_place,
            story_message=cmd.story_message,
            personal_dedication=cmd.personal_dedication,
            status="Success",
            result=result,
        )

        self.orders.add(order)

        return result


class GetLead(StandardOrderUseCase):
    def execute(self, query: queries.GetOrder) -> Order:
        order = self.messages.get(query.order_id)

        if order is None:  # pragma: no cover
            raise errors.OrderNotFound
        return order
