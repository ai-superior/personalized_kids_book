from dataclasses import dataclass
from enum import Enum

from domain.basic_types import Entity


class PreviewStatus(Enum):
    SELECTED = "SELECTED"
    UNSELECTED = "UNSELECTED"


@dataclass
class Preview(Entity):
    asset_ids: list[str]
    status: PreviewStatus
