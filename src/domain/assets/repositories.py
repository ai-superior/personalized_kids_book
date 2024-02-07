import abc

from domain.assets.model import Asset


class AssetRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, asset: Asset):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, asset_id: str) -> Asset:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_order_id(self, order_id: str) -> list[Asset]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Asset]:
        raise NotImplementedError
