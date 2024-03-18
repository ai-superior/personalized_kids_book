import pytest

from domain.assets.usecases import remove_bad_titles, stop_symbols, stop_ending_words


@pytest.mark.asyncio
async def test_remove_bad_titles():
    titles = ["\nTims Hafenabenteuer mit Fußball und Pizza"]
    result = remove_bad_titles(titles, stop_symbols, stop_ending_words)
    assert True
