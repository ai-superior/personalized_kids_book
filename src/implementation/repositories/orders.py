from domain.orders import model
from domain.orders.model import Order
from domain.orders.repositories import OrderRepository
from implementation.sql import SqlRepository


def convert_to_dict(obj):
    if isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return convert_to_dict(obj.__dict__)
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    else:
        return obj


def _model_to_db(orders: model.Order):
    return {
        "id": orders.id,
        "email": orders.email,
        "kids_name": orders.kids_name,
        "kids_gender": orders.kids_gender,
        "hair_color": orders.hair_color,
        "hair_length": orders.hair_length,
        "color_skin_tone": orders.color_skin_tone,
        "no_of_covers": orders.no_of_covers,
        "configs": convert_to_dict(orders.configs),
        "prompts": convert_to_dict(orders.prompts),
        "kids_date_of_birth": orders.kids_date_of_birth,
        "city": orders.city,
        "interest": orders.interest,
        "favourite_food": orders.favourite_food,
        "upcoming_life_event": orders.upcoming_life_event,
        "intent_message": orders.intent_message,
        "story_location": orders.story_location,
        "mood": orders.mood,
        "dedication": orders.dedication,
        "image": orders.image,
        "total_no_of_titles": orders.total_no_of_titles,
        "deal_id": orders.deal_id,
        "created_at": orders.created_at,
    }


def _db_to_model(order):
    if "_id" in order:
        del order["_id"]
    return Order.from_dict(order)


class OrderSqlRepository(OrderRepository, SqlRepository):
    async def add(self, order: Order):
        return await self.db["orders"].insert_one(_model_to_db(order))

    async def get(self, order_id: str) -> Order:
        document = await self.db["orders"].find_one({"id": order_id})
        return _db_to_model(document)

    async def update_deal_id(self, order_id: str, deal_id: str):
        document = await self.db["orders"].update_one(
            {"id": order_id}, {"$set": {"deal_id": deal_id}}
        )
        return await self.get(order_id)

    async def list(self) -> list[Order]:
        cursor = self.db["orders"].find({})
        orders = []
        async for document in cursor:
            orders.append(_db_to_model(document))
        return orders
