from features.accessibility import Accessibility
from features.html_based import (
    Advertisement,
    CookiesInHtml,
    EasylistAdult,
    EasyPrivacy,
    Paywalls,
)
from features.website_manager import WebsiteManager
from lib.logger import create_logger


def _test_feature(feature_class, html, expectation) -> tuple[bool, bool]:
    _logger = create_logger()

    feature = feature_class(_logger)

    feature.setup()
    website_manager = WebsiteManager.get_instance()

    website_manager.load_raw_data(html)

    data = feature.start()

    website_manager.reset()

    are_values_correct = set(data[feature.key]["values"]) == set(
        expectation[feature.key]["values"]
    )
    if are_values_correct and "excluded_values" in expectation[feature.key]:
        are_values_correct = (
            not data[feature.key]["values"]
            in expectation[feature.key]["excluded_values"]
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


# TODO: Currently, no solution to find these manually
def test_easylist_adult():
    feature = EasylistAdult
    feature._create_key(feature)
    html = {
        "html": "adlook.net\nver-pelis.net\n,geobanner.fuckbookhookups.com\n 22pixx.xyz \n trkinator.com \n soonbigo",
        "har": "",
        "url": "",
        "headers": "{}",
    }
    expected = {
        feature.key: {
            "values": [],
            "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test}
        }
    }

    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=feature, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough


def test_cookies_in_html():
    feature = CookiesInHtml
    feature._create_key(feature)
    html = {
        "html": """<div class='ast-small-footer-section ast-small-footer-section-1 ast-small-footer-section-equally ast-col-md-6 ast-col-xs-12' >
Copyright © 2021 Can You Block It<br><a href='https://www.iubenda.com/privacy-policy/24196256'
class='iubenda-black iubenda-embed" title="Privacy Policy ">Privacy Policy</a><script
type="3f8f8d2155875297dce02d6a-text/javascript">(function (w,d) {var loader = function ()
{var s = d.createElement("script"), tag = d.getElementsByTagName("script")[0];
s.src="https://cdn.iubenda.com/iubenda.js"; tag.parentNode.insertBefore(s,tag);};
if(w.addEventListener){w.addEventListener("load", loader, false);}else
if(w.attachEvent){w.attachEvent("onload", loader);}else{w.onload = loader;}})(window, document);
</script><a href="https://canyoublockit.com/disclaimer" rel="nofollow">Disclaimer</a>
<a href="https://www.iubenda.com/privacy-policy/24196256'" rel="nofollow">iubenda</a></div>
    """,
        "har": "",
        "url": "",
        "headers": "{}",
    }
    expected = {
        feature.key: {
            "values": ["||iubenda.com^$third-party"],
            "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test}
        }
    }

    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=feature, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough


def test_easy_privacy():
    feature = EasyPrivacy
    feature._create_key(feature)
    html = {
        "html": """<link rel='dns-prefetch' href='//www.googletagmanager.com' />
<script type="6cf3255238f69b4dbff7a6d1-text/javascript">!(function(o,n,t){t=o.createElement(n),
o=o.getElementsByTagName(n)[0],t.async=1,t.src=
"https://steadfastsystem.com/v2/0/mhdUYBjmgxDP_SQetgnGiancNmP1JIkDmyyXS_JPnDK2hCg_pE_-EVQw61Zu8YEjN6n_TSzbOSci6fkr2DxbJ4T-NH35ngHIfU1tGluTSrud8VFduwH1nKtjGf3-jvZWHD2MaGeUQ",
o.parentNode.insertBefore(t,o)})(document,"script"),
(function(o,n){o[n]=o[n]||function(){(o[n].q=o[n].q||[]).push(arguments)}})(window,"admiral");
!(function(n,e,r,t){function o(){if((function o(t){try{return(t=localStorage.getItem("v4ac1eiZr0"))&&0<t.split(",")[4]}
catch(n){}return!1})()){var t=n[e].pubads();typeof t.setTargeting===r&&t.setTargeting("admiral-engaged","true")}}
(t=n[e]=n[e]||{}).cmd=t.cmd||[],typeof t.pubads===r?o():typeof t.cmd.unshift===r?t.cmd.unshift(o):t.cmd.push(o)})
(window,"googletag","function");</script><script type="6cf3255238f69b4dbff7a6d1-text/javascript"
src='https://cdn.fluidplayer.com/v2/current/fluidplayer.min.js?ver=5.6' id='fluid-player-js-js'></script>
""",
        "har": "",
        "url": "",
        "headers": "{}",
    }
    expected = {
        feature.key: {
            "values": [
                "||googletagmanager.com^$image,third-party",
                "||steadfastsystem.com^$third-party",
            ],
            "excluded_values": [
                "https://cdn.fluidplayer.com/v2/current/fluidplayer.min.js?ver=5.6"
            ],
            "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test}
        }
    }

    are_values_correct, runs_fast_enough = _test_feature(
        feature_class=feature, html=html, expectation=expected
    )
    assert are_values_correct and runs_fast_enough
