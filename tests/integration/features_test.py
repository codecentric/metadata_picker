from features.html_based import Advertisement
from features.website_manager import WebsiteData, WebsiteManager
from lib.logger import create_logger

"""
Call each feature separately with known html+har etc.
Compare to what I expect
For now, this will fail
 
"""

# FIXME:
#  - ISSUE:
#   Somehow I cannot understand my own code anymore.
#       - What type is used where?
#       - Why is the code slow (taking more than a minute for a complete execution)
#          - What are the bottlenecks? Why are the bottlenecks there?
#       - I have landed at a certain architecture (inheritance, REST, APIs, containers)
#           - Why? Is that needed? Can I improve them somehow?
#   Right now I Cannot confidently say that I know what is going on in the code! Why are ads detected and why not? (applies to most/all features)
#       - What is the flow of data? Are datatypes observed?
#       - Did my solution hinder myself when scaling? Did I choose async/multiprocessing because I did not know better?
#   Acceptance tests are completely lacking
#       - Definition of Done (DoD)?
#       - How close/far am I?
#   Yesterday I was horribly confused
#       - basically I just did whatever came to my head, I was tired, emotional and therefore destructive (in that context)
#       - I potentially destroyed the main branch, a prod branch was created as a potential rescue
#   Due to the standalone
#       - I actually do not need the spiders anymore
#       - the service could get all urls from edu share and work through these
#       - independent microservice, all by itself, speed is less of an issue
#       - interfaces with edushare
#   Prod branch:
#       - I merge into this branch if the main branch fits to the acceptance tests and everything applies to DoD
#       - This is basically what I am showing to the customer
#   Other branches:
#       - Main, nice, but not meeting acceptance, DoD
#       - Dev, me working through tickets, this would merge into main
#       - other names: stuff I am developing and testing, for now, this goes into dev
#  - Goal:
#       - Be safe to show the service to the customer
#       - Find back structure and a clear line of work

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
