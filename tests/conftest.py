import os
from pathlib import Path

import pytest


@pytest.fixture
def chdir_root():
    current = Path(__file__)
    os.chdir(current.parent.parent)


@pytest.fixture
def tests_root():
    return Path(__file__).parent


@pytest.fixture
def fixture_root(tests_root):
    return tests_root / "fixtures"
