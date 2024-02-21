from dataclasses import dataclass
from typing import Literal

from domain.basic_types import Command


@dataclass
class CoverConfigs:
    quality: Literal["standard", "hd"] = "standard"
    model: str = "dall-e-3"


@dataclass
class TitleConfigs:
    temperature: float = 1.7
    max_tokens: int = 150
    model: str = "gpt-4-1106-preview"
    system_prompt: str = "You are a helpful assistant"


@dataclass
class Configs:
    cover_configs: CoverConfigs
    title_configs: TitleConfigs


@dataclass
class Prompt:
    cover_prompt: str = """Give me a standard Image"""
    title_prompt: str = """Give me a Standard Title"""


@dataclass(frozen=True)
class CreateOrder(Command):
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
    age: str
    gender: str
    hair_style: str
    configs: Configs
    prompts: Prompt
    no_of_covers: int = 2
