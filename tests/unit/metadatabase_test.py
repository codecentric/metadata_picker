from unittest import mock

import adblockparser
import pytest

from features.metadata_base import MetadataBase, ProbabilityDeterminationMethod
from features.website_manager import WebsiteData


@pytest.fixture
def metadatabase(mocker):
    logger = mocker.MagicMock()
    return MetadataBase(logger)


"""
--------------------------------------------------------------------------------
"""


def test_init(metadatabase: MetadataBase, mocker):
    assert metadatabase.tag_list == []
    assert metadatabase.tag_list_last_modified == ""
    assert metadatabase.tag_list_expires == 0
    assert metadatabase.key == "metadata_base"
    assert metadatabase.url == ""
    assert metadatabase.comment_symbol == ""
    assert not metadatabase.evaluate_header
    assert isinstance(metadatabase._logger, mocker.MagicMock)


"""
--------------------------------------------------------------------------------
"""


def test_start(metadatabase: MetadataBase, mocker):
    html_content = "html_content"
    header = {"header": "empty_header"}
    metadatabase.key = "test_key"
    start_spy = mocker.spy(metadatabase, "_start")
    values = metadatabase.start()

    values_has_only_one_key = len(values.keys()) == 1

    assert isinstance(values, dict)
    assert metadatabase.key in values.keys()
    assert values_has_only_one_key
    assert values[metadatabase.key]["values"] == []

    if "tag_list_last_modified" in values[metadatabase.key].keys():
        assert values[metadatabase.key]["tag_list_last_modified"] == ""
        assert values[metadatabase.key]["tag_list_expires"] == 0
    assert start_spy.call_count == 1
    assert start_spy.call_args_list[0][1] == {
        "website_data": WebsiteData(
            html="", values=[], headers={}, raw_header=""
        )
    }

    with mock.patch(
        "features.metadata_base.WebsiteManager"
    ) as mocked_website_manager:
        mocked_website_manager.get_instance().website_data = WebsiteData(
            html=html_content, raw_header="", headers=header
        )
        _ = metadatabase.start()
        assert start_spy.call_args_list[1][1] == {
            "website_data": WebsiteData(
                html=html_content, values=[], headers=header
            )
        }


"""
--------------------------------------------------------------------------------
"""


def test_under_start(metadatabase: MetadataBase, mocker):
    html_content = "html_content"
    header = "header"
    processed_header = {header: header}

    work_header_spy = mocker.spy(metadatabase, "_work_header")
    work_html_content_spy = mocker.spy(metadatabase, "_work_html_content")

    metadatabase.evaluate_header = False
    website_data = WebsiteData(
        html=html_content, values=[], headers=processed_header
    )

    values = metadatabase._start(website_data=website_data)

    assert isinstance(values, dict)
    assert work_header_spy.call_count == 0
    assert work_html_content_spy.call_count == 1

    metadatabase.evaluate_header = True
    _ = metadatabase._start(website_data=website_data)
    assert work_header_spy.call_count == 1
    assert work_html_content_spy.call_count == 1


"""
--------------------------------------------------------------------------------
"""


def test_setup(metadatabase: MetadataBase, mocker):
    metadatabase._download_tag_list = mocker.AsyncMock(return_value=[])
    metadatabase._download_multiple_tag_lists = mocker.AsyncMock(
        return_value=[]
    )
    extract_date_from_list_spy = mocker.spy(
        metadatabase, "_extract_date_from_list"
    )
    prepare_tag_spy = mocker.spy(metadatabase, "_prepare_tag_list")

    metadatabase.setup()
    assert metadatabase._download_tag_list.call_count == 0
    assert metadatabase._download_multiple_tag_lists.call_count == 0
    assert extract_date_from_list_spy.call_count == 0
    assert prepare_tag_spy.call_count == 0

    metadatabase.url = "hello"
    metadatabase.setup()
    assert metadatabase._download_tag_list.call_count == 1
    assert metadatabase._download_multiple_tag_lists.call_count == 0
    assert extract_date_from_list_spy.call_count == 0
    assert prepare_tag_spy.call_count == 0

    metadatabase.url = ""
    metadatabase.urls = ["Hello1", "Hello2"]
    metadatabase._download_tag_list.return_value = ["empty_list"]
    metadatabase.setup()
    assert metadatabase._download_tag_list.call_count == 1
    assert metadatabase._download_multiple_tag_lists.call_count == 1
    assert extract_date_from_list_spy.call_count == 0
    assert prepare_tag_spy.call_count == 0

    metadatabase.tag_list = ["empty_list"]
    metadatabase.urls = []
    metadatabase.setup()
    assert metadatabase._download_tag_list.call_count == 1
    assert metadatabase._download_multiple_tag_lists.call_count == 1
    assert extract_date_from_list_spy.call_count == 1
    assert prepare_tag_spy.call_count == 1


"""
--------------------------------------------------------------------------------
"""


def _create_sample_easylist() -> list:
    easylist = [
        "! *** easylist:easylist/easylist_general_block.txt ***",
        r"/adv_horiz.",
        r"@@||imx.to/dropzone.js$script",
        r"||testimx.to/dropzone.js$script",
        r"||testimx2.to/dropzone.js",
    ]

    return easylist


def _create_sample_urls() -> list:
    url_to_be_blocked = [
        ("https://www.dictionary.com/", False),
        ("/adv_horiz.", True),
        ("imx.to/dropzone.js", False),
        ("testimx.to/dropzone.js", False),
        ("testimx2.to/dropzone.js", True),
    ]
    return url_to_be_blocked


def test_easylist_filter():
    urls_to_be_blocked = _create_sample_urls()

    rules = adblockparser.AdblockRules(_create_sample_easylist())

    for url, to_be_blocked in urls_to_be_blocked:
        result = rules.should_block(url)  # "http://ads.example.com"
        assert result == to_be_blocked


"""
--------------------------------------------------------------------------------
"""


@pytest.mark.parametrize(
    "values, decision_threshold, expected_decision, expected_probability",
    [
        ([], -1, False, 0),
        (
            [0.5],
            -1,
            False,
            1,
        ),
        (
            [0.5, 1],
            -1,
            False,
            1,
        ),
        (
            [0.5],
            0.5,
            True,
            1,
        ),
        (
            [0.5],
            1,
            False,
            1,
        ),
    ],
)
def test_decide_single(
    metadatabase: MetadataBase,
    values,
    decision_threshold,
    expected_decision,
    expected_probability,
):
    website_data = WebsiteData()

    website_data.values = values
    metadatabase.decision_threshold = decision_threshold
    metadatabase.probability_determination_method = (
        ProbabilityDeterminationMethod.SINGLE_OCCURRENCE
    )
    decision, probability = metadatabase._decide(website_data=website_data)

    assert decision == expected_decision
    assert probability == expected_probability


"""
--------------------------------------------------------------------------------
"""


@pytest.mark.parametrize(
    "values, decision_threshold, expected_decision, expected_probability, raw_links",
    [
        (
            [0.5],
            0,
            False,
            0,
            [],
        ),
        (
            [0.5, 1, 1, 1],
            0,
            True,
            1,
            [1, 1, 1, 1],
        ),
        (
            [0.5],
            0,
            True,
            0.25,
            [1, 1, 1, 1],
        ),
        (
            [0.5],
            0.5,
            False,
            0.5,
            [1, 1, 1, 1],
        ),
    ],
)
def test_decide_number_of_elements(
    metadatabase: MetadataBase,
    values,
    decision_threshold,
    expected_decision,
    expected_probability,
    raw_links,
):
    website_data = WebsiteData()

    website_data.values = values
    website_data.raw_links = raw_links
    metadatabase.decision_threshold = decision_threshold
    metadatabase.probability_determination_method = (
        ProbabilityDeterminationMethod.NUMBER_OF_ELEMENTS
    )
    decision, probability = metadatabase._decide(website_data=website_data)

    assert decision == expected_decision
    assert probability == expected_probability


"""
--------------------------------------------------------------------------------
"""


@pytest.mark.parametrize(
    "values, decision_threshold, expected_decision, expected_probability",
    [
        (
            [0.5],
            0,
            True,
            0.5,
        ),
        (
            [0.5],
            0.5,
            False,
            0,
        ),
        (
            [0.75, 0.1],
            0.5,
            True,
            0.5,
        ),
    ],
)
def test_first_value(
    metadatabase: MetadataBase,
    values,
    decision_threshold,
    expected_decision,
    expected_probability,
):
    website_data = WebsiteData()

    website_data.values = values
    metadatabase.decision_threshold = decision_threshold
    metadatabase.probability_determination_method = (
        ProbabilityDeterminationMethod.FIRST_VALUE
    )
    decision, probability = metadatabase._decide(website_data=website_data)

    assert decision == expected_decision
    assert probability == expected_probability


"""
--------------------------------------------------------------------------------
"""


@pytest.mark.parametrize(
    "values, decision_threshold, expected_decision, expected_probability",
    [
        (
            [0.5],
            0,
            True,
            0.5,
        ),
        (
            [0.5],
            0.5,
            False,
            0,
        ),
        (
            [0.75, 0.25],
            0.5,
            False,
            0,
        ),
        (
            [0.6, 0.8],
            0.5,
            True,
            0.4,
        ),
    ],
)
def test_mean_value(
    metadatabase: MetadataBase,
    values,
    decision_threshold,
    expected_decision,
    expected_probability,
):
    website_data = WebsiteData()

    website_data.values = values
    metadatabase.decision_threshold = decision_threshold
    metadatabase.probability_determination_method = (
        ProbabilityDeterminationMethod.MEAN_VALUE
    )
    decision, probability = metadatabase._decide(website_data=website_data)

    assert decision == expected_decision
    assert probability == expected_probability


"""
--------------------------------------------------------------------------------
"""


@pytest.mark.parametrize(
    "values, decision_threshold, expected_decision, expected_probability, false_list",
    [
        ([0.5], 1, True, 1, [0]),
        ([0.5], 1, False, 1, [0.5]),
        ([0.5, 0.1, 0, "hello"], 1, False, 1, ["hello"]),
        ([0.5, 0.1, 0, "hello"], 1, True, 1, ["hell"]),
        ([0.5, 0.1, 0, "hello"], 1, True, 1, ["0"]),
        ([0.5, 0.1, 0, "hello"], 1, False, 1, ["0", "hello"]),
    ],
)
def test_false_list(
    metadatabase: MetadataBase,
    values,
    decision_threshold,
    expected_decision,
    expected_probability,
    false_list,
):
    website_data = WebsiteData()

    website_data.values = values
    metadatabase.false_list = false_list
    metadatabase.decision_threshold = decision_threshold
    metadatabase.probability_determination_method = (
        ProbabilityDeterminationMethod.FALSE_LIST
    )
    decision, probability = metadatabase._decide(website_data=website_data)

    assert decision == expected_decision
    assert probability == expected_probability
