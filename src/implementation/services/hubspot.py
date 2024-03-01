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
        async with httpx.AsyncClient(headers=self.headers) as client:
            return await client.get(f"{self.host}/crm/v3/objects/contacts")

    async def get_contact(self, contact_id: str):
        async with httpx.AsyncClient(headers=self.headers) as client:
            return await client.get(f"{self.host}/crm/v3/objects/contacts/{contact_id}")

    async def create_deal(self, deal: Deal):
        async with httpx.AsyncClient(headers=self.headers) as client:
            body = {
                "properties": {
                    "amount": str(deal.amount),
                    "dealname": deal.name,
                    "pipeline": "default",
                    "dealstage": deal.stage,
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

    async def get_deal(self, deal_id: str):
        async with httpx.AsyncClient(headers=self.headers) as client:
            return await client.get(f"{self.host}/crm/v3/objects/deals/{deal_id}")

    async def get_deals(self):
        async with httpx.AsyncClient(headers=self.headers) as client:
            return await client.get(f"{self.host}/crm/v3/objects/deals")

    async def create_contact(self, contact: Contact):
        async with httpx.AsyncClient(headers=self.headers) as client:
            body = {
                "properties": {
                    "firstname": contact.first_name,
                    "lastname": contact.last_name,
                    "email": contact.email,
                }
            }
            return await client.post(f"{self.host}/crm/v3/objects/contacts", json=body)
