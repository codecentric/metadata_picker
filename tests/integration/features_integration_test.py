from features.html_based import Advertisement, Paywalls
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
        data[feature.key]["values"] == expectation[feature.key]["values"]
    )
    runs_fast_enough = (
        data[feature.key]["time_required"]
        <= expectation[feature.key]["runs_within"]
    )
    return are_values_correct, runs_fast_enough


def test_advertisement():
    feature = Advertisement
    feature._create_key(feature)
    html = {
        "html": "<script src='/xlayer/layer.php?uid='></script>",
        "har": "",
        "url": "",
        "headers": "{}",
    }
    expected = {
        feature.key: {
            "values": ["/xlayer/layer.php?uid=$script"],
            "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test
        },
    }
    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=feature, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough


def test_paywalls():
    feature = Paywalls
    html = {
        "html": "<paywall></paywalluser>",
        "har": "",
        "url": "",
        "headers": "{}",
    }
    expected = {
        feature.key: {
            "values": ["paywall", "paywalluser"],
            "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test
        },
    }

    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=feature, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough
