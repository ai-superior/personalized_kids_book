from domain.orders import model
from domain.orders.model import Order
from domain.orders.repositories import OrderRepository
from implementation.sql import SqlRepository


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
    }


def _db_to_model(order):
    return Order(
        id=order["id"],
        email=order["email"],
        name=order["name"],
        city=order["city"],
        birthday=order["birthday"],
        favourite_food=order["favourite_food"],
        interests=order["interests"],
        event_to_come=order["event_to_come"],
        skin_tone=order["skin_tone"],
        hair_color=order["hair_color"],
        hair_length=order["hair_length"],
        kids_photo=order["kids_photo"],
        favourite_place=order["favourite_place"],
        story_message=order["story_message"],
        personal_dedication=order["personal_dedication"],
    )


class OrderSqlRepository(OrderRepository, SqlRepository):
    def add(self, order: Order):
        return self.db["orders"].insert_one(_model_to_db(order))

    def get(self, order_id: str) -> Order:
        return _db_to_model(self.db["orders"].find_one({"id": order_id}))

    def list(self) -> list[Order]:
        orders = self.db["orders"].find({})
        return [_db_to_model(msg) for msg in orders]
