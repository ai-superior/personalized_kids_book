from openai import OpenAI

from domain.leads.services import LLMProcessor


class OpenAIAPI(LLMProcessor):
    def __init__(self):
        self.client = OpenAI()

    async def ask_for_text(self, prompt: str):
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.9,
            max_tokens=150,
        )
        return response

    async def ask_for_image(self, prompt: str):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response
