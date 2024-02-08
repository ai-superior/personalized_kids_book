import abc


class LLMProcessor(abc.ABC):
    @abc.abstractmethod
    async def ask_for_text(self, prompt: str, quantity: int):
        ...

    @abc.abstractmethod
    async def ask_for_image(self, prompt: str):
        ...
