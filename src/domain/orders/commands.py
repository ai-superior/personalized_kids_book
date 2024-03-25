from dataclasses import dataclass
from typing import Literal

from domain.basic_types import Command
from domain.orders.model import Prompt, Configs


@dataclass
class CoverConfigs:
    quality: Literal["standard", "hd"] = "standard"
    model: str = "dall-e-3"


@dataclass(frozen=True)
class CreateOrder(Command):
    email: str
    name: str
    city: str
    birthday: str
    favourite_food: str
    interests: str
    intent: str
    story_location: str
    event_to_come: str
    skin_tone: str
    hair_color: str
    hair_length: str
    kids_photo: str
    favourite_place: str
    story_message: str
    personal_dedication: str
    age: str
    gender: str
    hair_style: str
    configs: Configs
    prompts: Prompt
    no_of_covers: int = 2
    total_no_of_titles: int = 5
