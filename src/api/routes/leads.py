from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.orders import commands, usecases, model

router = APIRouter(prefix="/orders")


@router.post("/")
async def create_lead(cmd: commands.CreateOrder) -> model.Result:
    di = DependencyInjector.get()
    usecase = usecases.CreateOrder(di.orders(), di.gpt())
    return await usecase.execute(cmd)
