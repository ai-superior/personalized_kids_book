import pytest

from dependencies import DependencyInjector
from domain.previews.model import Preview
from domain.previews.repositories import PreviewRepository


@pytest.mark.asyncio
async def test_get_all_previews(preview: Preview):
    repo: PreviewRepository = DependencyInjector.get().previews()
    previews = await repo.list()
    assert len(previews) >= 1


@pytest.mark.asyncio
async def test_get_preview(preview: Preview):
    repo: PreviewRepository = DependencyInjector.get().previews()
    lead_collection = await repo.get(preview.id)
    assert lead_collection.id == preview.id
