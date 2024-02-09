from dataclasses import dataclass
from typing import Optional

from domain.basic_types import Command


@dataclass(frozen=True)
class CreateAsset(Command):
    order_id: str
    no_of_covers: Optional[int] = 2
