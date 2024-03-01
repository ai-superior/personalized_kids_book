import abc

from domain.orders.model import LLMTextConfig, LLMImageConfig


class LLMProcessor(abc.ABC):
    @abc.abstractmethod
    async def ask_for_text(self, prompt: str, quantity: int, configs: LLMTextConfig):
        ...

    @abc.abstractmethod
    async def ask_for_image(self, prompt: str, configs: LLMImageConfig):
        ...


class CRM(abc.ABC):
    @abc.abstractmethod
    async def get(self):
        ...
