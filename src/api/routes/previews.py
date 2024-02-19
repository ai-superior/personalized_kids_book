from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.previews import commands, usecases, model, queries

router = APIRouter(prefix="/previews")


@router.post("/")
def create_preview(cmd: commands.CreatePreview) -> model.Preview:
    di = DependencyInjector.get()
    usecase = usecases.CreatePreview(di.previews(), di.assets())
    return usecase.execute(cmd)


@router.get("/")
def get_previews() -> list[model.Preview]:
    di = DependencyInjector.get()
    usecase = usecases.GetPreviews(di.previews())
    return usecase.execute()


@router.get("/preview_id/{preview_id}")
def get_preview_by_preview_id(preview_id: str) -> model.Preview:
    di = DependencyInjector.get()
    usecase = usecases.GetPreview(di.previews())
    return usecase.execute(queries.GetPreview(preview_id=preview_id))


@router.get("/order_id/{order_id}")
def get_preview_by_order_id(order_id: str) -> list[model.Preview]:
    di = DependencyInjector.get()
    usecase = usecases.GetPreviewByOrderId(di.previews())
    return usecase.execute(queries.GetPreviewsByOrderId(order_id=order_id))
