import pytest

from implementation.services.open_ai import OpenAIAPI


@pytest.mark.asyncio
async def test_ask_for_text():
    open_ai = OpenAIAPI()
    dummy_prompt = 'This is a test message. Only Reply "Hello"'
    response = await open_ai.ask_for_text(dummy_prompt)
    message = response.choices[0].message.content
    assert message == "Hello"


@pytest.mark.asyncio
async def test_ask_for_image():
    open_ai = OpenAIAPI()
    response = await open_ai.ask_for_image(
        "This is test message. Give me a standard test image"
    )
    image_url = response.data[0].url

    assert image_url.startswith("https://")
