from openai import OpenAI

from domain.orders.commands import CreateOrder
from domain.orders.services import LLMProcessor


class OpenAIAPI(LLMProcessor):
    def __init__(self):
        self.client = OpenAI()

    # TODO: This was done in haste, we should not have domain objects in here, integrations tests not possible, to go ahead and change this structure later
    async def ask_for_text(self, prompt: str, quantity: int, configs: CreateOrder):
        response = self.client.chat.completions.create(
            model=configs.configs.title_configs.model,
            messages=[
                {
                    "role": "system",
                    "content": configs.configs.title_configs.system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            temperature=configs.configs.title_configs.temperature,
            max_tokens=configs.configs.title_configs.max_tokens,
            n=quantity,
        )
        return response

    async def ask_for_image(self, prompt: str, configs: CreateOrder):
        response = self.client.images.generate(
            model=configs.configs.cover_configs.model,
            prompt=prompt,
            size="1792x1024",
            quality=configs.configs.cover_configs.quality,
            n=1,
        )
        return response
