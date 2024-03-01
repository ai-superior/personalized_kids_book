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
        "name": orders.name,
        "city": orders.city,
        "birthday": orders.birthday,
        "favourite_food": orders.favourite_food,
        "interests": orders.interests,
        "event_to_come": orders.event_to_come,
        "skin_tone": orders.skin_tone,
        "hair_color": orders.hair_color,
        "hair_length": orders.hair_length,
        "kids_photo": orders.kids_photo,
        "story_message": orders.story_message,
        "favourite_place": orders.favourite_place,
        "personal_dedication": orders.personal_dedication,
        "created_at": orders.created_at,
        "gender": orders.gender,
        "age": orders.age,
        "hair_style": orders.hair_style,
        "no_of_covers": orders.no_of_covers,
        "configs": convert_to_dict(orders.configs),
        "prompts": convert_to_dict(orders.prompts),
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

    async def list(self) -> list[Order]:
        cursor = self.db["orders"].find({})
        orders = []
        async for document in cursor:
            orders.append(_db_to_model(document))
        return orders
