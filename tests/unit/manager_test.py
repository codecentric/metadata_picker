from unittest import mock

import pytest

from manager import Manager


@pytest.fixture
def manager(mocker):
    Manager._create_logger = mocker.MagicMock()
    Manager._create_api = mocker.MagicMock()
    Manager._logger = mocker.MagicMock()
    Manager.setup = mocker.MagicMock()

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
    assert len(manager.metadata_extractors) == 16
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


"""
--------------------------------------------------------------------------------
"""


def test_handle_content(manager: Manager, mocker):
    request = {}

    empty_header = "empty_header"
    empty_html = "empty_html"
    empty_url = "empty_url"

    with mock.patch("manager.WebsiteManager") as mocked_website_manager:
        manager._extract_meta_data = mocker.MagicMock()

        manager.handle_content(request)

        assert manager._extract_meta_data.call_count == 0
        assert (
            mocked_website_manager.get_instance().load_raw_data.call_count == 0
        )
        assert mocked_website_manager.get_instance().reset.call_count == 0

        allow_list = {}
        request = {
            "some_uuid": {
                "html": empty_html,
                "headers": empty_header,
                "allow_list": allow_list,
                "url": empty_url,
            }
        }

        manager.manager_to_api_queue = mocker.MagicMock()
        manager.handle_content(request)

        assert manager._extract_meta_data.call_count == 1
        assert (
            mocked_website_manager.get_instance().load_raw_data.call_count == 1
        )
        assert mocked_website_manager.get_instance().reset.call_count == 1

        is_extract_meta_data_called_with_empty_html = (
            manager._extract_meta_data.call_args_list[0][0][0] == allow_list
        )
        assert is_extract_meta_data_called_with_empty_html
