import abc

from domain.orders.model import Order


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, order: Order):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, order_id: str) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    async def list(self) -> list[Order]:
        raise NotImplementedError
