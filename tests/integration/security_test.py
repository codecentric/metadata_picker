import json
import os

from features.security import Security
from features.website_manager import WebsiteData
from lib.logger import create_logger

if "PRE_COMMIT" in os.environ:
    from integration.features_integration_test import _test_feature
else:
    from tests.integration.features_integration_test import _test_feature

security_tags = {
    "vary": ["accept-encoding", "cookie"],
    "x-frame-options": ["same_origin"],
    "content-security-policy": ["same_origin"],
}


def test_content_security_policy():
    feature = Security
    feature._create_key(feature)

    html = {
        "html": "empty_html",
        "har": "",
        "url": "",
        "headers": json.dumps(security_tags),
    }
    expected = {
        feature.key: {
            "values": ["x-frame-options", "content-security-policy"],
            "excluded_values": ["deny"],
            "runs_within": 2,  # time the evaluation may take AT MAX -> acceptance test}
        }
    }

    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=feature, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough


"""
--------------------------------------------------------------------------------
"""


def test_decide():
    _logger = create_logger()

    security = Security(_logger)

    website_data = WebsiteData()
    website_data.values = [
        "x-frame-options",
        "content-security-policy",
        "vary",
    ]
    expected_decision = True
    expected_probability = 1.0

    print(security.tags)
    security.tags = security_tags
    print(security.tags)

    decision, probability = security._decide(website_data=website_data)

    assert probability == expected_probability
    assert decision == expected_decision
