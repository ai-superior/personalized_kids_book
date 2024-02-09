from domain.previews.usecases import CreatePreview


def test_fuse_images():
    cover_image_url = (
        "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/mock_cover.png"
    )
    char_image_url = "https://ai-childrens-book-assets.s3.eu-central-1.amazonaws.com/mock_character.png"

    fused_url = CreatePreview.fuse_images(
        cover_image_url, char_image_url, "Title Header", "test"
    )
    assert len(fused_url) > 1
