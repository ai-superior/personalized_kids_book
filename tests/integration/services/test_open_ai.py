import pytest

from domain.orders.services import LLMTextConfig, LLMImageConfig
from implementation.services.open_ai import OpenAIAPI


@pytest.mark.asyncio
async def test_ask_for_text():
    open_ai = OpenAIAPI()
    dummy_prompt = 'This is a test message. Only Reply "Hello"'
    response = await open_ai.ask_for_text(
        quantity=1,
        prompt=dummy_prompt,
        configs=LLMTextConfig(
            system_prompt="You are a good assistant!",
            model="gpt-4-1106-preview",
            temperature=1.7,
            max_tokens=150,
        ),
    )
    message = response.choices[0].message.content
    assert message.strip() == "Hello"


@pytest.mark.asyncio
async def test_ask_for_image():
    open_ai = OpenAIAPI()
    response = await open_ai.ask_for_image(
        prompt="Generate a standard Image",
        configs=LLMImageConfig(quality="standard", model="dall-e-3"),
    )
    image_url = response.data[0].url

    assert image_url.startswith("https://")
