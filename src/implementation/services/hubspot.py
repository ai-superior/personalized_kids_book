import httpx

from domain.orders.model import Contact, Deal
from domain.orders.services import CRM
from settings import SETTINGS


class HubSpot(CRM):
    def __init__(self):
        self.host = SETTINGS.hubspot.host
        self.headers = {
            "Authorization": f"Bearer {SETTINGS.hubspot.access_token}",
            "Content-Type": "application/json",
        }

    async def get_contacts(self):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.get(f"{self.host}/crm/v3/objects/contacts")

    async def get_contact(self, contact_id: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.get(f"{self.host}/crm/v3/objects/contacts/{contact_id}")

    async def create_deal(self, deal: Deal, order):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            body = {
                "properties": {
                    "amount": str(deal.amount),
                    "dealname": deal.name,
                    "pipeline": "default",
                    "dealstage": deal.stage,
                    "order_details": order,
                },
                "associations": [
                    {
                        "to": {"id": deal.contact_id},
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 3,
                            }
                        ],
                    },
                ],
            }
            return await client.post(f"{self.host}/crm/v3/objects/deals", json=body)

    async def update_deal(self, deal_id: str, assets=None, preview=None):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            body = {"properties": {}}

            if assets is not None:
                body["properties"]["asset_details"] = assets

            if preview is not None:
                body["properties"]["preview_details"] = preview

            return await client.patch(
                f"{self.host}/crm/v3/objects/deals/{deal_id}", json=body
            )

    async def get_deal(self, deal_id: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.get(f"{self.host}/crm/v3/objects/deals/{deal_id}")

    async def get_deals(self):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.get(f"{self.host}/crm/v3/objects/deals")

    async def create_contact(self, contact: Contact):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            body = {
                "properties": {
                    "firstname": contact.name,
                    "email": contact.email,
                }
            }
            return await client.post(f"{self.host}/crm/v3/objects/contacts", json=body)

    async def create_group(self, group_name: str, group_label: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            body = {
                "name": group_name,
                "label": group_label,
                "displayOrder": -1,
            }
            return await client.post(
                f"{self.host}/crm/v3/properties/deal/groups", json=body
            )

    async def delete_group(self, group_name: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.delete(
                f"{self.host}/crm/v3/properties/deal/groups/{group_name}"
            )

    async def get_group(self, group_name: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.get(
                f"{self.host}/crm/v3/properties/deal/groups/{group_name}"
            )

    async def create_property(
        self, group_name: str, property_name: str, field_type: str, data_type: str
    ):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            body = {
                "fieldType": field_type,
                "groupName": group_name,
                "label": property_name,
                "name": property_name,
                "type": data_type,
            }
            return await client.post(f"{self.host}/crm/v3/properties/deal", json=body)

    async def create_dropdown_property(
        self, group_name: str, property_name: str, possible_values: list
    ):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            options = []
            for value in possible_values:
                options.append({"label": value, "value": value})
            body = {
                "fieldType": "select",
                "options": options,
                "groupName": group_name,
                "label": property_name,
                "name": property_name,
                "type": "enumeration",
            }
            return await client.post(f"{self.host}/crm/v3/properties/deal", json=body)

    async def delete_property(self, property_name: str):
        async with httpx.AsyncClient(headers=self.headers, timeout=300.0) as client:
            return await client.delete(
                f"{self.host}/crm/v3/properties/deal/{property_name}"
            )
