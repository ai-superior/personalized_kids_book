from dataclasses import dataclass
from typing import Optional

from domain.basic_types import Command


@dataclass(frozen=True)
class CreatePreview(Command):
    order_id: str
    asset_ids: Optional[list[str]]
