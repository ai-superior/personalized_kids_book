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
        created_at=order["created_at"],
        gender=order["gender"],
        age=order["age"],
        hair_style=order["hair_style"],
        no_of_covers=order["no_of_covers"],
        configs=order["configs"],
        prompts=order["prompts"],
    )


class OrderSqlRepository(OrderRepository, SqlRepository):
    def add(self, order: Order):
        return self.db["orders"].insert_one(_model_to_db(order))

    def get(self, order_id: str) -> Order:
        return _db_to_model(self.db["orders"].find_one({"id": order_id}))

    def list(self) -> list[Order]:
        orders = self.db["orders"].find({})
        return [_db_to_model(msg) for msg in orders]
