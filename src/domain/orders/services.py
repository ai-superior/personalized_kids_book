import abc

from domain.orders.commands import CreateOrder


class LLMProcessor(abc.ABC):
    @abc.abstractmethod
    async def ask_for_text(self, prompt: str, quantity: int, configs: CreateOrder):
        ...

    @abc.abstractmethod
    async def ask_for_image(self, prompt: str, configs: CreateOrder):
        ...
