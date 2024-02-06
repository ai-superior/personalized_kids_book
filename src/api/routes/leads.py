from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.leads import commands, usecases, model

router = APIRouter(prefix="/leads")


@router.post("/")
async def create_lead(cmd: commands.CreateLeads) -> model.Result:
    di = DependencyInjector.get()
    usecase = usecases.CreateLead(di.leads(), di.gpt())
    return await usecase.execute(cmd)
