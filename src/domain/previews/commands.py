from dataclasses import dataclass

from domain.basic_types import Command


@dataclass(frozen=True)
class CreatePreview(Command):
    order_id: str
    asset_ids: list[str]
