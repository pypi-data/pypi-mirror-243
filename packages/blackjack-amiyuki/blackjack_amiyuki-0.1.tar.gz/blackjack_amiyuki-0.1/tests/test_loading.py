import pytest
import typing
from blackjack.state.loading import AssetLoader
from . import FromFixture


@pytest.fixture
def assets() -> AssetLoader:
    return AssetLoader()


def test_expected_assets(assets: FromFixture[AssetLoader]):
    # 52 cards + 1 back + 1 front
    assert assets.expected_files == 55
