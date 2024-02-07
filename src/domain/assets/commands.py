from dataclasses import dataclass
from typing import Optional

from domain.basic_types import Command


@dataclass(frozen=True)
class CreateAsset(Command):
    order_id: str
    quantity: Optional[int] = 2
