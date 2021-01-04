from features.html_based import Advertisement
from features.website_manager import WebsiteManager
from lib.logger import create_logger

# TODO Check other features, e.g. adult:
# html = {
#     "html": "9content.com\n,ytimm.com\n,boyzshop.com/affimages/",
#     "har": "",
#     "url": "",
# }
# expected = {
#     "easylist_adult": {
#         "values": ["9content.com", "ad_slot="],
#         "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test}
#     }
# }


def _test_feature(feature_class, html, expectation) -> tuple[bool, bool]:
    _logger = create_logger()

    feature = feature_class(_logger)

    feature.setup()
    website_manager = WebsiteManager.get_instance()

    website_manager.load_raw_data(html)

    data = feature.start()

    website_manager.reset()

    are_values_correct = (
        data["advertisement"]["values"]
        == expectation["advertisement"]["values"]
    )
    runs_fast_enough = (
        data["advertisement"]["time_required"]
        <= expectation["advertisement"]["runs_within"]
    )
    return are_values_correct, runs_fast_enough


def test_advertisement():
    html = {
        "html": "<script src='/xlayer/layer.php?uid='></script>",
        "har": "",
        "url": "",
        "headers": "{}",
    }
    expected = {
        "advertisement": {
            "values": ["/xlayer/layer.php?uid=$script"],
            "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test
        },
    }
    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=Advertisement, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough
