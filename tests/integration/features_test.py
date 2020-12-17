"""
Call each feature separately with known html+har etc.
Compare to what I expect
For now, this will fail
"""
from features.html_based import Advertisement
from features.website_manager import WebsiteData, WebsiteManager
from lib.logger import create_logger

html = {
    "html": "9content.com\n,ytimm.com\n,boyzshop.com/affimages/",
    "har": "",
    "url": "",
}
expected = {
    "easylist_adult": {
        "values": ["9content.com", "ad_slot="],
        "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test}
    }
}
html = {
    "html": "ad_block, ad_slot= mallorcash.com admanmedia murkymouse.online",
    "har": "",
    "url": "",
    "headers": "{}",
}
expected = {
    "advertisement": {"values": ["ad_block", "ad_slot="]},
    "runs_within": 10,  # time the evaluation may take AT MAX -> acceptance test
}


# TODO: Have some websites evaluated, store the evaluation and compare with future evaluations

_logger = create_logger()

advertisement = Advertisement(_logger)

advertisement.setup()
website_manager = WebsiteManager.get_instance()
website_manager.load_raw_data(html)
website_data = WebsiteData(html=html["html"], raw_header="", headers={})
website_data.raw_links = [html["html"]]
website_data.html = html["html"]
print(website_manager.website_data)
print(website_data)
data = advertisement.start()

print(data)
