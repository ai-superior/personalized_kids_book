from dataclasses import dataclass
from enum import Enum

from domain.basic_types import Entity


class PreviewStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class Preview(Entity):
    asset_ids: list[str]
    is_approved: bool
    status: PreviewStatus
