from unittest import mock

import pytest

from manager import Manager


@pytest.fixture
def manager(mocker):
    Manager._create_logger = mocker.MagicMock()
    Manager._create_api = mocker.MagicMock()
    Manager._logger = mocker.MagicMock()

    with mock.patch("manager.Manager.run"):
        manager = Manager()
    return manager


"""
--------------------------------------------------------------------------------
"""


def test_init(manager: Manager, mocker):
    run_spy = mocker.spy(manager, "run")
    assert manager._create_logger.call_count == 1
    assert manager._create_api.call_count == 1
    assert run_spy.call_count == 0
    assert len(manager.metadata_extractors) == 13
    assert manager.run_loop


"""
--------------------------------------------------------------------------------
"""


def test_run(manager: Manager, mocker):
    manager.run = Manager.run
    manager.get_api_request = mocker.MagicMock()

    manager.run_loop = False
    manager.run(manager)
    assert manager.get_api_request.call_count == 0

    # TODO Cannot mock the while loop sufficiently well, yet
    # manager.run_loop = True
    # manager.get_api_request.side_effect = _setting_run_loop()
    # print("run")
    # manager.run(manager)
