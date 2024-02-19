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
    return Preview(
        id=preview["id"],
        order_id=preview["order_id"],
        status=preview["status"],
        asset_ids=preview["asset_ids"],
        created_at=preview["created_at"],
        is_approved=preview["is_approved"],
        title=preview["title"],
        cover_image_url=preview["cover_image_url"],
        character_image_url=preview["character_image_url"],
        fused_image_url=preview["fused_image_url"],
    )


class PreviewSqlRepository(PreviewRepository, SqlRepository):
    def add(self, preview: Preview):
        return self.db["previews"].insert_one(_model_to_db(preview))

    def get(self, preview_id: str) -> Preview:
        return _db_to_model(self.db["previews"].find_one({"id": preview_id}))

    def get_by_order_id(self, order_id: str) -> list[Preview]:
        previews = self.db["previews"].find({"order_id": order_id})
        return [_db_to_model(msg) for msg in previews]

    def list(self) -> list[Preview]:
        previews = self.db["previews"].find({})
        return [_db_to_model(msg) for msg in previews]
