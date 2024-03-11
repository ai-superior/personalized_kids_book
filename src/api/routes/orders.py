from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.assets import commands as asset_commands
from domain.assets import usecases as asset_usecases
from domain.orders import commands, usecases, model, queries
from domain.previews import usecases as preview_usecases

router = APIRouter(prefix="/orders")


@router.post("/")
async def create_order(cmd: commands.CreateOrder) -> model.Order:
    di = DependencyInjector.get()
    order_usecase = usecases.CreateOrder(di.orders())
    asset_usecase = asset_usecases.CreateAsset(di.assets(), di.orders(), di.gpt())
    preview_usecases.CreatePreview(di.previews(), di.assets())
    orders = await order_usecase.execute(cmd)
    await asset_usecase.execute(
        asset_commands.CreateAsset(order_id=orders.id, additional_params=cmd)
    )
    return orders


@router.get("/")
async def get_orders() -> list[model.Order]:
    di = DependencyInjector.get()
    usecase = usecases.GetOrders(di.orders())
    return await usecase.execute()


@router.get("/{order_id}")
async def get_order(order_id: str) -> model.Order:
    di = DependencyInjector.get()
    usecase = usecases.GetOrder(di.orders())
    return await usecase.execute(queries.GetOrder(order_id=order_id))


@router.get("/order_status/{order_id}")
async def get_assets_status(order_id: str) -> bool:
    di = DependencyInjector.get()
    usecase = usecases.GetOrderStatus(di.orders(), di.assets())
    return await usecase.execute(queries.GetOrderStatus(order_id=order_id))
