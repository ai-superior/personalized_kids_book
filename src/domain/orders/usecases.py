import abc
import json
import re

from domain.assets.repositories import AssetRepository
from domain.basic_types import UseCase, dataclass_to_dict
from domain.orders import queries, errors, commands
from domain.orders.model import Order, Contact, Deal
from domain.orders.repositories import OrderRepository
from domain.orders.services import CRM


def extract_existing_contact_id_from_error(error_message):
    pattern = r"Existing ID: (\d+)"
    match = re.search(pattern, error_message)
    if match:
        existing_contact_id = int(match.group(1))
        return existing_contact_id
    else:
        return None


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
        if len(assets) >= total_titles + total_covers + 1:
            return True
        else:
            return False


class CreateOrder(UseCase):
    def __init__(self, orders: OrderRepository, crm: CRM):
        super().__init__()
        self.orders = orders
        self.crm = crm

    async def execute(self, cmd: commands.CreateOrder):
        order = Order(
            email=cmd.email,
            kids_name=cmd.kids_name,
            city=cmd.city,
            kids_date_of_birth=cmd.kids_date_of_birth,
            favourite_food=cmd.favourite_food,
            interest=cmd.interest,
            upcoming_life_event=cmd.upcoming_life_event,
            color_skin_tone=cmd.color_skin_tone,
            hair_color=cmd.hair_color,
            hair_length=cmd.hair_length,
            image=cmd.image,
            dedication=cmd.dedication,
            kids_gender=cmd.kids_gender,
            age=cmd.age,
            no_of_covers=cmd.no_of_covers,
            total_no_of_titles=cmd.total_no_of_titles,
            prompts=cmd.prompts,
            configs=cmd.configs,
            intent_message=cmd.intent_message,
            story_location=cmd.story_location,
        )
        await self.orders.add(order)
        contact_response = await self.crm.create_contact(
            contact=Contact(email=cmd.email, name=cmd.kids_name)
        )
        if contact_response.status_code == 201:
            contact_id = contact_response.json()["id"]
        else:
            contact_id = extract_existing_contact_id_from_error(
                contact_response.json()["message"]
            )
        deal_response = await self.crm.create_deal(
            deal=Deal(
                amount="30", name=order.id, stage="contractsent", contact_id=contact_id
            ),
            order=json.dumps(dataclass_to_dict(order)),
        )
        await self.orders.update_deal_id(
            order_id=order.id, deal_id=deal_response.json()["id"]
        )
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
