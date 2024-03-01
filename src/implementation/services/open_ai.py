from openai import OpenAI

from domain.orders.model import LLMTextConfig, LLMImageConfig
from domain.orders.services import LLMProcessor


class OpenAIAPI(LLMProcessor):
    async def ask_for_text(self, prompt: str, quantity: int, configs: LLMTextConfig):
        response = self.client.chat.completions.create(
            model=configs.model,
            messages=[
                {
                    "role": "system",
                    "content": configs.system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            temperature=configs.temperature,
            max_tokens=configs.max_tokens,
            n=quantity,
        )
        return response

    async def ask_for_image(self, prompt: str, configs: LLMImageConfig):
        response = self.client.images.generate(
            model=configs.model,
            prompt=prompt,
            size="1792x1024",
            quality=configs.quality,
            n=1,
        )
        return response

    def __init__(self):
        self.client = OpenAI()
