from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.assets import commands, usecases, model, queries

router = APIRouter(prefix="/assets")


@router.post("/")
def create_asset(cmd: commands.CreateAsset) -> list[model.Asset]:
    di = DependencyInjector.get()
    usecase = usecases.CreateAsset(di.assets())
    return usecase.execute(cmd)


@router.get("/asset_id/{asset_id}")
def get_asset_by_asset_id(asset_id: str) -> model.Asset:
    di = DependencyInjector.get()
    usecase = usecases.GetAsset(di.assets())
    return usecase.execute(queries.GetAsset(asset_id=asset_id))


@router.get("/order_id/{order_id}")
def get_asset_by_order_id(order_id: str) -> list[model.Asset]:
    di = DependencyInjector.get()
    usecase = usecases.GetAssetByOrderId(di.assets())
    return usecase.execute(queries.GetAssetByOrderId(order_id=order_id))
