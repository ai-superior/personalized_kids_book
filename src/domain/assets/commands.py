from dataclasses import dataclass

from domain.basic_types import Command
from domain.orders.commands import CreateOrder


@dataclass(frozen=True)
class CreateAsset(Command):
    order_id: str
    additional_params: CreateOrder
