from dataclasses import dataclass
from typing import Optional

from typing_extensions import Literal

from domain.basic_types import Entity


@dataclass
class LLMTextConfig:
    model: str
    system_prompt: str
    temperature: float
    max_tokens: int


@dataclass
class Contact:
    email: str
    name: str


@dataclass
class Deal:
    amount: str
    name: str
    stage: str
    contact_id: str


@dataclass
class LLMImageConfig:
    model: str
    quality: Literal["standard", "hd"]


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


@dataclass
class Order(Entity):
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
    image: Optional[str] = None
    total_no_of_titles: int = 5
    deal_id: Optional[str] = None
