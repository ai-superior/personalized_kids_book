from dataclasses import dataclass

from domain.basic_types import Command


@dataclass(frozen=True)
class CreatePreview(Command):
    asset_ids: list[str]
