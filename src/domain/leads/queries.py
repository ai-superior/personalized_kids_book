from dataclasses import dataclass

from domain.basic_types import Query


@dataclass(frozen=True)
class GetLead(Query):
    request_id: str
