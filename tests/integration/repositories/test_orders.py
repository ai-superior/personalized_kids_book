import pytest

from dependencies import DependencyInjector
from domain.orders.model import Order
from domain.orders.repositories import OrderRepository


@pytest.mark.asyncio
async def test_get_all_orders(order: Order):
    repo: OrderRepository = DependencyInjector.get().orders()
    orders = await repo.list()
    assert len(orders) >= 1


@pytest.mark.asyncio
async def test_get_order(order: Order):
    repo: OrderRepository = DependencyInjector.get().orders()
    order_collection = await repo.get(order.id)
    assert order_collection.id == order.id
