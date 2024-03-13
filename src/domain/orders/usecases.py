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
    # Define a regex pattern to search for the existing contact ID
    pattern = r"Existing ID: (\d+)"
    # Search for the pattern in the error message
    match = re.search(pattern, error_message)
    if match:
        # If a match is found, return the ID as an integer
        existing_contact_id = int(match.group(1))
        return existing_contact_id
    else:
        # If no match is found, return None
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
        if len(assets) >= total_titles + total_covers - 1:
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
        contact_response = await self.crm.create_contact(
            contact=Contact(email=cmd.email, name=cmd.name)
        )
        if contact_response.status_code == "200":
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
