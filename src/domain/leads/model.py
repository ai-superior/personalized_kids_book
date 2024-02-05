from dataclasses import dataclass

from domain.basic_types import Entity


@dataclass
class Lead(Entity):
    email: str
    name: str
    city: str
    birthday: str
    favourite_food: str
    likes: str
    activities: str
    skin_tone: str
    hair_color: str
    hair_length: str
    kids_photo: str
