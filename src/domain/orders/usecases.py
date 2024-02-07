import abc

from domain.basic_types import UseCase
from domain.orders import queries, errors, commands
from domain.orders.model import Order
from domain.orders.repositories import OrderRepository


class StandardOrderUseCase(UseCase, abc.ABC):
    def __init__(self, messages: OrderRepository):
        super().__init__()
        self.messages = messages


class CreateOrder(UseCase):
    def __init__(self, orders: OrderRepository):
        super().__init__()
        self.orders = orders

    def execute(self, cmd: commands.CreateOrder):
        order = Order(
            email=cmd.email,
            name=cmd.name,
            city=cmd.city,
            birthday=cmd.birthday,
            favourite_food=cmd.favourite_food,
            interests=cmd.interests,
            event_to_come=cmd.event_to_come,
            skin_tone=cmd.skin_tone,
            hair_color=cmd.hair_color,
            hair_length=cmd.hair_length,
            kids_photo=cmd.kids_photo,
            favourite_place=cmd.favourite_place,
            story_message=cmd.story_message,
            personal_dedication=cmd.personal_dedication,
        )
        self.orders.add(order)
        return order


class GetOrder(StandardOrderUseCase):
    def execute(self, query: queries.GetOrder) -> Order:
        order = self.messages.get(query.order_id)

        if order is None:  # pragma: no cover
            raise errors.OrderNotFound
        return order
