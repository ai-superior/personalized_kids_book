from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.assets import commands as asset_commands
from domain.assets import usecases as asset_usecases
from domain.assets.model import Asset, AssetType
from domain.orders import commands, usecases, model, queries
from domain.previews import usecases as preview_usecases

router = APIRouter(prefix="/orders")


def getting_first_asset_ids(assets: list[Asset]):
    asset_ids = []
    for asset in assets:
        if asset.type == AssetType.TITLE.value:
            asset_ids.append(asset.id)
            break

    for asset in assets:
        if asset.type == AssetType.BACKGROUND_IMAGE.value:
            asset_ids.append(asset.id)
            break

    for asset in assets:
        if asset.type == AssetType.CHARACTER_IMAGE.value:
            asset_ids.append(asset.id)
            break
    return asset_ids


@router.post("/")
async def create_order(cmd: commands.CreateOrder) -> model.Order:
    di = DependencyInjector.get()
    order_usecase = usecases.CreateOrder(di.orders())
    asset_usecase = asset_usecases.CreateAsset(di.assets(), di.orders(), di.gpt())
    preview_usecase = preview_usecases.CreatePreview(di.previews(), di.assets())
    orders = order_usecase.execute(cmd)
    assets = await asset_usecase.execute(
        asset_commands.CreateAsset(order_id=orders.id, additional_params=cmd)
    )
    # asset_ids = getting_first_asset_ids(assets)
    # preview_usecase.execute(
    #     preview_commands.CreatePreview(order_id=orders.id, asset_ids=asset_ids)
    # )
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
