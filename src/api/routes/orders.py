from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.assets import commands as asset_commands
from domain.assets import usecases as asset_usecases
from domain.orders import commands, usecases, model, queries

router = APIRouter(prefix="/orders")


@router.post("/")
async def create_order(cmd: commands.CreateOrder) -> model.Order:
    di = DependencyInjector.get()
    order_usecase = usecases.CreateOrder(di.orders())
    asset_usecase = asset_usecases.CreateAsset(di.assets(), di.orders(), di.gpt())
    orders = order_usecase.execute(cmd)
    await asset_usecase.execute(
        asset_commands.CreateAsset(order_id=orders.id, additional_params=cmd)
    )
    return orders


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
