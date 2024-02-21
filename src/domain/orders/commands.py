from dataclasses import dataclass
from typing import Literal

from domain.basic_types import Command


@dataclass()
class CoverConfigs:
    quality: Literal["standard", "hd"] = "standard"
    model: str = "dall-e-3"


@dataclass()
class TitleConfigs:
    temperature: float = 1.7
    max_tokens: int = 150
    model: str = "gpt-4-1106-preview"
    system_prompt: str = "You are a helpful assistant"


@dataclass()
class Configs:
    cover_configs: CoverConfigs
    title_configs: TitleConfigs


@dataclass()
class Prompt:
    cover_prompt: str = """
# Generate a scenery Cover for a children book in a 3D pixar cartoon style. Here is a title that describes the story:

Title: {{generated_title}}

# Additional notes:
1. Image orientation: horizontal
2. Important: Ensure the image is free from any textual elements.
3. Important: It is only background, without people or animals or any other characters on the image.
"""
    title_prompt: str = """
Act as a creative German book author. Create a title for the children book story.

Title should adhere to following rules:
1. Language - German
2. Included Child's name
3. Word-playful and engaging 
4. Title should be based on following information about the child:

Child's information below:
Name is {{name}}
City is {{city}}
Birthday is {{birthday}}
Favorite food is {{favourite_food}}
Interests are {{interests}}
Favorite place is {{favourite_place}}
An expected event is {{event_to_come}}


Here are Examples of the book titles with desired format and suitable presentation of result:
a. Mutige Alma und die Osterferien auf dem Pferdehof
b. Alma, die Weißwurstprinzessin und das Turnier der musikalischen Freunde
c. Alma, die Weißwurst-Detektivin und das Geheimnis der verschwundenen Osterhasen


The title length must not be more than 10 words.
"""


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
