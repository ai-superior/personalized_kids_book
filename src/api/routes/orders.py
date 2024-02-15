from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.orders import commands, usecases, model, queries

router = APIRouter(prefix="/orders")


@router.post("/")
def create_order(cmd: commands.CreateOrder) -> model.Order:
    di = DependencyInjector.get()
    usecase = usecases.CreateOrder(di.orders())
    return usecase.execute(cmd)


@router.get("/")
def get_orders() -> list[model.Order]:
    di = DependencyInjector.get()
    usecase = usecases.GetOrders(di.orders())
    return usecase.execute()


@router.get("/{order_id}")
def get_order(order_id: str) -> model.Order:
    di = DependencyInjector.get()
    usecase = usecases.GetOrder(di.orders())
    return usecase.execute(queries.GetOrder(order_id=order_id))
