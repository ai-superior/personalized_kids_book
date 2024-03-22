import asyncio

from fastapi import APIRouter

from dependencies import DependencyInjector
from domain.orders.model import Deal
from domain.previews import commands, usecases, model, queries

router = APIRouter(prefix="/previews")


@router.post("/")
async def create_preview(cmd: commands.CreatePreview) -> model.Preview:
    di = DependencyInjector.get()
    usecase = usecases.CreatePreview(di.previews(), di.assets(), di.crm(), di.orders())
    return await usecase.execute(cmd)


@router.get("/")
async def get_previews() -> list[model.Preview]:
    di = DependencyInjector.get()
    usecase = usecases.GetPreviews(di.previews())
    return await usecase.execute()


@router.get("/preview_id/{preview_id}")
async def get_preview_by_preview_id(preview_id: str) -> model.Preview:
    di = DependencyInjector.get()
    usecase = usecases.GetPreview(di.previews())
    return await usecase.execute(queries.GetPreview(preview_id=preview_id))


@router.get("/order_id/{order_id}")
async def get_preview_by_order_id(order_id: str) -> list[model.Preview]:
    di = DependencyInjector.get()
    usecase = usecases.GetPreviewByOrderId(
        previews=di.previews(), orders=di.orders(), crm=di.crm()
    )
    return await usecase.execute(queries.GetPreviewsByOrderId(order_id=order_id))


@router.put("/approve/preview_id")
async def approve_preview(preview_id: str) -> model.Preview:
    di = DependencyInjector.get()
    usecase = usecases.ApprovePreview(
        previews=di.previews(), crm=di.crm(), orders=di.orders()
    )
    return await usecase.execute(queries.ApprovePreview(preview_id=preview_id))


@router.post("/test_preview")
async def get_test_preview():
    await asyncio.sleep(3)
    return {
        "image_url": "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/mock_preview.png"
    }


@router.get("/test_hubspot_deal")
async def create_hubspot_deal():
    random_deal = Deal(
        name="test_deal", contact_id="1951", amount="30", stage="contractsent"
    )
    di = DependencyInjector.get()
    deal_response = await di.crm().create_deal(deal=random_deal, order="test")
    return deal_response.json()
