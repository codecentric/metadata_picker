from features.metadata_base import MetadataBase


class Advertisement(MetadataBase):
    url: str = "https://easylist.to/easylist/easylist.txt"
    key: str = "ads"


class EasyPrivacy(MetadataBase):
    urls: list = [
        "https://easylist.to/easylist/easyprivacy.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_general.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_allowlist.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_allowlist_international.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_specific.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_specific_international.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_trackingservers.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_trackingservers_international.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_thirdparty.txt",
        "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_thirdparty_international.txt",
    ]


class IETracker(MetadataBase):
    url: str = "https://easylist-downloads.adblockplus.org/easyprivacy.tpl"
    key: str = "internet_explorer_tracker"
    comment_symbol = "#"


class Cookies(MetadataBase):
    url: str = "https://easylist-downloads.adblockplus.org/easylist-cookie.txt"
    key: str = "cookies"


class FanboyAnnoyance(MetadataBase):
    url: str = "https://easylist.to/easylist/fanboy-annoyance.txt"
    key: str = "fanboy_annoyance"


class FanboySocialMedia(MetadataBase):
    url: str = "https://easylist.to/easylist/fanboy-social.txt"
    key: str = "fanboy_social"


class AntiAdBlock(MetadataBase):
    url: str = (
        "https://easylist-downloads.adblockplus.org/antiadblockfilters.txt"
    )
    key: str = "anti_adblock"


class AntiAdBlockGerman(MetadataBase):
    url: str = (
        "https://github.com/easylist/antiadblockfilters/blob/master/antiadblockfilters/antiadblock_german.txt"
    )
    key: str = "antiadblock_german"


class AntiAdBlockEnglish(MetadataBase):
    url: str = (
        "https://github.com/easylist/antiadblockfilters/blob/master/antiadblockfilters/antiadblock_english.txt"
    )
    key: str = "antiadblock_english"


class EasylistGermany(MetadataBase):
    urls: list = [
        "https://easylist.to/easylistgermany/easylistgermany.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_adservers.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_adservers_popup.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_allowlist.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_allowlist_dimensions.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_allowlist_general_hide.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_allowlist_popup.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_general_block.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_general_block_popup.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_general_hide.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_specific_block.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_specific_block_popup.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_specific_hide.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_thirdparty.txt",
        "https://github.com/easylist/easylistgermany/blob/master/easylistgermany/easylistgermany_thirdparty_popup.txt"
    ]
    key: str = "easylist_germany"


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
