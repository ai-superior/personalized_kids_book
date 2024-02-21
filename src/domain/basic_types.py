import abc
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Self
from uuid import uuid4


@dataclass(kw_only=True)
class Entity:
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )  # pragma: no cover

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        entity = cls(**data)
        return entity


@dataclass(frozen=True)
class Query(abc.ABC):
    pass


@dataclass(frozen=True)
class Command(abc.ABC):
    pass


@dataclass(frozen=True)
class Event(abc.ABC):
    pass


Alert = Command | Event


@dataclass(frozen=True)
class Error(Exception):
    msg: str


class UseCase(abc.ABC):
    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError


class SortOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"
