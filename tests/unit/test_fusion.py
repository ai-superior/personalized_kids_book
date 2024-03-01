import pytest

from domain.previews.usecases import CreatePreview


@pytest.mark.asyncio
async def test_fuse_images():
    cover_image_url = (
        "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/test_cover2.png"
    )
    char_image_url = "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/characters_imgs/01b-01b.png"

    fused_url = await CreatePreview.fuse_images(
        cover_image_url=cover_image_url,
        char_image_url=char_image_url,
        title="Hello World how are you doing? I am doing fine. Thanks",
        output_file_name="test",
    )
    assert len(fused_url) > 1
    assert True
