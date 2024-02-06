from dataclasses import dataclass
from typing import Optional

from domain.basic_types import Entity


@dataclass
class Result:
    title: str
    cover_url: str
    character_url: str
    final_result_url: str


@dataclass
class Lead(Entity):
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
    status: Optional[str] = None
    result: Optional[Result] = None
