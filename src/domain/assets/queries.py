from dataclasses import dataclass

from domain.basic_types import Query


@dataclass(frozen=True)
class GetAsset(Query):
    asset_id: str
