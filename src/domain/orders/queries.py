from dataclasses import dataclass

from domain.basic_types import Query


@dataclass(frozen=True)
class GetOrder(Query):
    order_id: str
