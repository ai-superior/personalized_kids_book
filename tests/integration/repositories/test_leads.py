from dependencies import DependencyInjector

from domain.orders.model import Order
from domain.orders.repositories import OrderRepository


def test_get_all_leads(order: Order):
    repo: OrderRepository = DependencyInjector.get().orders()
    leads = repo.list()
    assert len(leads) >= 1


def test_get_lead(order: Order):
    repo: OrderRepository = DependencyInjector.get().orders()
    lead_collection = repo.get(order.id)
    assert lead_collection.id == order.id
