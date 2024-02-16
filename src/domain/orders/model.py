from dataclasses import dataclass

from domain.basic_types import Entity


@dataclass
class Order(Entity):
    email: str
    name: str
    city: str
    birthday: str
    favourite_food: str
    interests: str
    event_to_come: str
    skin_tone: str
    hair_color: str
    hair_length: str
    kids_photo: str
    favourite_place: str
    story_message: str
    personal_dedication: str
    gender: str
    age: str
    hair_style: str
