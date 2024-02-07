from dataclasses import dataclass
from enum import Enum

from domain.basic_types import Entity


class AssetType(Enum):
    CHARACTER_IMAGE = "CHARACTER_IMAGE"
    BACKGROUND_IMAGE = "BACKGROUND_IMAGE"
    TITLE = "TITLE"


class AssetStatus(Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"


@dataclass
class Asset(Entity):
    order_id: str
    type: AssetType
    status: AssetStatus
