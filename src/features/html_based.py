from bs4 import BeautifulSoup

from features.EasylistFilter import EasyFilter
from features.MetadataBase import MetadataBase


class Advertisement(MetadataBase):
    url: str = "https://easylist.to/easylist/easylist.txt"
    key: str = "ads"
    comment_symbol = "!"

    def _start(self, html_content: str, header: dict) -> dict:
        soup = BeautifulSoup(html_content, "html.parser")
        raw_links = list({a["href"] for a in soup.find_all(href=True)})

        easylist = self.tag_list

        print(raw_links)
        found_matches = []
        for url in raw_links:
            adblock_filter = EasyFilter(easylist)
            found_matches.append(adblock_filter.match(url))

            print(f"For url '{url}' found these matches: '{found_matches}'")
        return {"values": found_matches}


class Tracker(MetadataBase):
    url: str = "https://easylist.to/easylist/easyprivacy.txt"
    key: str = "tracker"
    comment_symbol = "!"


class IETracker(MetadataBase):
    url: str = "https://easylist-downloads.adblockplus.org/easyprivacy.tpl"
    key: str = "internet_explorer_tracker"
    comment_symbol = "#"


class Cookies(MetadataBase):
    url: str = "https://easylist-downloads.adblockplus.org/easylist-cookie.txt"
    key: str = "cookies"
    comment_symbol = "!"


class EasylistGermany(MetadataBase):
    url: str = "https://easylist.to/easylistgermany/easylistgermany.txt"
    key: str = "easylist_germany"
    comment_symbol = "!"


class FanboyAnnoyance(MetadataBase):
    url: str = "https://easylist.to/easylist/fanboy-annoyance.txt"
    key: str = "fanboy_annoyance"
    comment_symbol = "!"


class FanboySocialMedia(MetadataBase):
    url: str = "https://easylist.to/easylist/fanboy-social.txt"
    key: str = "fanboy_social"
    comment_symbol = "!"


class AntiAdBlock(MetadataBase):
    url: str = (
        "https://easylist-downloads.adblockplus.org/antiadblockfilters.txt"
    )
    key: str = "anti_adblock"
    comment_symbol = "!"


class Paywalls(MetadataBase):
    tag_list = ["paywall", "paywalluser"]
    key: str = "paywall"


class ContentSecurityPolicy(MetadataBase):
    tag_list = ["Content-Security-Policy"]
    key: str = "content_security_policy"
    evaluate_header = True


class IFrameEmbeddable(MetadataBase):
    tag_list = ["X-Frame-Options"]
    key: str = "iframe_embeddable"
    evaluate_header = True


class PopUp(MetadataBase):
    tag_list = [
        "popup",
        "popuptext",
        "modal",
        "modal fade",
        "modal-dialog",
        "interstitial",
        "Interstitial",
    ]
    key = "popup"
