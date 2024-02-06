import abc

from domain.orders.model import Order


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, order: Order):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, order_id: str) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Order]:
        raise NotImplementedError
