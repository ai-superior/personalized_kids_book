from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.assets import usecases as asset_usecases, commands as asset_commands
from domain.orders import commands, usecases, model, queries

router = APIRouter(prefix="/orders")


@router.post("/")
async def create_order(cmd: commands.CreateOrder) -> model.Order:
    di = DependencyInjector.get()
    usecase1 = usecases.CreateOrder(di.orders())
    usecase2 = asset_usecases.CreateAsset(di.assets(), di.orders(), di.gpt())
    orders = usecase1.execute(cmd)
    await usecase2.execute(
        asset_commands.CreateAsset(order_id=orders.id, no_of_covers=cmd.no_of_covers)
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
