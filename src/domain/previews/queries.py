from dataclasses import dataclass

from domain.basic_types import Query


@dataclass(frozen=True)
class GetPreview(Query):
    preview_id: str


@dataclass(frozen=True)
class GetPreviewsByOrderId(Query):
    order_id: str
