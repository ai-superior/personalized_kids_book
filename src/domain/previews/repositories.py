import abc

from domain.previews.model import Preview


class PreviewRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, preview: Preview):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, preview_id: str) -> Preview:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Preview]:
        raise NotImplementedError
