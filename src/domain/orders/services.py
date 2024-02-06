import abc


class LLMProcessor(abc.ABC):
    @abc.abstractmethod
    async def ask_for_text(self, prompt: str):
        ...

    @abc.abstractmethod
    async def ask_for_image(self, prompt: str):
        ...
