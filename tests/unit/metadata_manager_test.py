import asyncio
import time
from logging import Logger

import pytest

from features.metadata_manager import MetadataManager


@pytest.fixture
def metadata_manager():
    manager = MetadataManager.get_instance()
    return manager


"""
--------------------------------------------------------------------------------
"""


def test_init(metadata_manager: MetadataManager):
    print(test_init)
    assert isinstance(metadata_manager._logger, Logger)
    assert len(metadata_manager.metadata_extractors) == 22
