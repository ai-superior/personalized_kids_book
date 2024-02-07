from dependencies import DependencyInjector

from domain.orders.model import Order
from domain.orders.repositories import OrderRepository


def test_get_all_orders(order: Order):
    repo: OrderRepository = DependencyInjector.get().orders()
    orders = repo.list()
    assert len(orders) >= 1


def test_get_order(order: Order):
    repo: OrderRepository = DependencyInjector.get().orders()
    order_collection = repo.get(order.id)
    assert order_collection.id == order.id
