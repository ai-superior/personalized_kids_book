from dataclasses import dataclass
from enum import Enum
from typing import Optional

from domain.basic_types import Entity


class PreviewStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class Preview(Entity):
    asset_ids: list[str]
    order_id: str
    status: PreviewStatus
    is_approved: Optional[bool] = None
    title: Optional[str] = None
    cover_image_url: Optional[str] = None
    character_image_url: Optional[str] = None
    fused_image_url: Optional[str] = None
