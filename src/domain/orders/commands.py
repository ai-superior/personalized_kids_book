from dataclasses import dataclass
from typing import Literal, Optional

from domain.basic_types import Command
from domain.orders.model import Prompt, Configs


@dataclass
class CoverConfigs:
    quality: Literal["standard", "hd"] = "standard"
    model: str = "dall-e-3"


@dataclass(frozen=True)
class CreateOrder(Command):
    email: str
    kids_name: str
    kids_gender: str
    hair_color: str
    hair_length: str
    color_skin_tone: str
    no_of_covers: int
    configs: Configs
    prompts: Prompt
    kids_date_of_birth: Optional[str] = None
    age: Optional[str] = "2-6"
    city: Optional[str] = None
    interest: Optional[str] = None
    favourite_food: Optional[str] = None
    upcoming_life_event: Optional[str] = None
    intent_message: Optional[str] = None
    story_location: Optional[str] = None
    mood: Optional[str] = None
    dedication: Optional[str] = None
    image: str = None

    total_no_of_titles: int = 5
