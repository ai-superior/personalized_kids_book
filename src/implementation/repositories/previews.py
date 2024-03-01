from domain.previews import model
from domain.previews.model import Preview
from domain.previews.repositories import PreviewRepository
from implementation.sql import SqlRepository


def _model_to_db(previews: model.Preview):
    return {
        "id": previews.id,
        "order_id": previews.order_id,
        "status": previews.status,
        "asset_ids": previews.asset_ids,
        "created_at": previews.created_at,
        "is_approved": previews.is_approved,
        "title": previews.title,
        "cover_image_url": previews.cover_image_url,
        "character_image_url": previews.character_image_url,
        "fused_image_url": previews.fused_image_url,
    }


def _db_to_model(preview):
    if "_id" in preview:
        del preview["_id"]
    return preview


class PreviewSqlRepository(PreviewRepository, SqlRepository):
    async def add(self, preview: Preview):
        return await self.db["previews"].insert_one(_model_to_db(preview))

    async def get(self, preview_id: str) -> Preview:
        document = await self.db["previews"].find_one({"id": preview_id})
        return _db_to_model(document)

    async def get_by_order_id(self, order_id: str) -> list[Preview]:
        cursor = self.db["previews"].find({"order_id": order_id})
        previews = []
        async for document in cursor:
            previews.append(_db_to_model(document))
        return previews

    async def list(self) -> list[Preview]:
        cursor = self.db["previews"].find({})
        previews = []
        async for document in cursor:
            previews.append(_db_to_model(document))
        return previews
