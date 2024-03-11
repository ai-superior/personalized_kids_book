import abc

from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase
from domain.orders import queries, errors, commands
from domain.orders.model import Order
from domain.orders.repositories import OrderRepository


class StandardOrderUseCase(UseCase, abc.ABC):
    def __init__(self, orders: OrderRepository):
        super().__init__()
        self.orders = orders


class GetOrderStatus(UseCase):
    def __init__(self, orders: OrderRepository, assets: AssetRepository):
        super().__init__()
        self.orders = orders
        self.assets = assets

    async def execute(self, query: queries.GetOrderStatus):
        order = await self.orders.get(query.order_id)
        assets = await self.assets.get_by_order_id(query.order_id)
        total_titles = (
            int(order.total_no_of_titles) if order.total_no_of_titles is not None else 0
        )
        total_covers = int(order.no_of_covers) if order.no_of_covers is not None else 0
        if len(assets) >= total_titles + total_covers - 1:
            return True
        else:
            return False


class CreateOrder(UseCase):
    def __init__(self, orders: OrderRepository):
        super().__init__()
        self.orders = orders

    async def execute(self, cmd: commands.CreateOrder):
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
            gender=cmd.gender,
            hair_style=cmd.hair_style,
            age=cmd.age,
            no_of_covers=cmd.no_of_covers,
            total_no_of_titles=cmd.total_no_of_titles,
            prompts=cmd.prompts,
            configs=cmd.configs,
        )
        await self.orders.add(order)
        return order


class GetOrder(StandardOrderUseCase):
    async def execute(self, query: queries.GetOrder) -> Order:
        order = await self.orders.get(query.order_id)

        if order is None:  # pragma: no cover
            raise errors.OrderNotFound
        return order


class GetOrders(StandardOrderUseCase):
    async def execute(self) -> list[Order]:
        orders = await self.orders.list()
        return orders
