import abc

from domain.orders.model import LLMTextConfig, LLMImageConfig, Contact, Deal


class LLMProcessor(abc.ABC):
    @abc.abstractmethod
    async def ask_for_text(self, prompt: str, quantity: int, configs: LLMTextConfig):
        ...

    @abc.abstractmethod
    async def ask_for_image(self, prompt: str, configs: LLMImageConfig):
        ...


class CRM(abc.ABC):
    @abc.abstractmethod
    async def create_contact(self, contact: Contact):
        ...

    @abc.abstractmethod
    async def get_contacts(self):
        ...

    @abc.abstractmethod
    async def get_contact(self, contact_id: str):
        ...

    @abc.abstractmethod
    async def create_deal(self, deal: Deal, order):
        ...

    @abc.abstractmethod
    async def get_deals(self):
        ...

    @abc.abstractmethod
    async def get_deal(self, deal_id: str):
        ...
