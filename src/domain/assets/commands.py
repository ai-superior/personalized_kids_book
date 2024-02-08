from dataclasses import dataclass
from typing import Optional

from domain.basic_types import Command


@dataclass(frozen=True)
class CreateAsset(Command):
    order_id: str
    no_of_titles: Optional[int] = 2
    no_of_cover_images: Optional[int] = 2
