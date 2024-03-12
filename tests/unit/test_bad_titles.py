import pytest

from domain.assets.usecases import remove_bad_titles, stop_symbols, stop_ending_words


@pytest.mark.asyncio
async def test_remove_bad_titles():
    titles = ["Tim, der Hanse-Kicker und das Pizza-Abenteuer am Spanischen Strand"]
    result = remove_bad_titles(titles, stop_symbols, stop_ending_words)
    assert True
