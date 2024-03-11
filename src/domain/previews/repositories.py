import abc

from domain.previews.model import Preview


class PreviewRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, preview: Preview):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, preview_id: str) -> Preview:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_order_id(self, order_id: str) -> list[Preview]:
        raise NotImplementedError

    @abc.abstractmethod
    async def list(self) -> list[Preview]:
        raise NotImplementedError

    @abc.abstractmethod
    async def approve_preview(self, preview_id: str) -> Preview:
        raise NotImplementedError

    @abc.abstractmethod
    async def disapprove_preview(self, preview: str) -> Preview:
        raise NotImplementedError
