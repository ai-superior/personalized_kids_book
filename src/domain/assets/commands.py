from dataclasses import dataclass

from domain.basic_types import Command


@dataclass(frozen=True)
class CreateAsset(Command):
    order_id: str
