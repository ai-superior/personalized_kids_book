from dataclasses import dataclass
from enum import Enum
from typing import Optional

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
    prompt: Optional[str] = None
    value: Optional[str] = None
    type: Optional[AssetType] = None
    status: Optional[AssetStatus] = None
