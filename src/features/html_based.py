from features.metadata_base import MetadataBase


class Advertisement(MetadataBase):
    url: str = "https://easylist.to/easylist/easylist.txt"
    key: str = "ads"


class EasyPrivacy(MetadataBase):
    url: str = "https://easylist.to/easylist/easyprivacy.txt"
    key: str = "easyprivacy"


class EasyprivacyGeneral(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_general.txt"
    key: str = "easyprivacy_general"


class EasyprivacyAllowlist(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_allowlist.txt"
    key: str = "easyprivacy_allowlist"


class EasyprivacyAllowlistInternational(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_allowlist_international.txt"
    key: str = "easyprivacy_allowlist_international"


class EasyprivacySpecific(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_specific.txt"
    key: str = "easyprivacy_specific"


class EasyprivacySpecificInternational(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_specific_international.txt"
    key: str = "easyprivacy_specific_international"


class EasyprivacyThirdparty(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_thirdparty.txt"
    key: str = "easyprivacy_thirdparty"


class EasyprivacyThirdpartyInternational(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_thirdparty_international.txt"
    key: str = "easyprivacy_thirdparty_international"


class EasyprivacyTrackingservers(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_trackingservers.txt"
    key: str = "easyprivacy_trackingservers"


class EasyprivacyTrackingserversInternational(MetadataBase):
    url: str = "https://github.com/easylist/easylist/blob/master/easyprivacy/easyprivacy_trackingservers_international.txt"
    key: str = "easyprivacy_trackingservers_international"


class IETracker(MetadataBase):
    url: str = "https://easylist-downloads.adblockplus.org/easyprivacy.tpl"
    key: str = "internet_explorer_tracker"
    comment_symbol = "#"


class Cookies(MetadataBase):
    url: str = "https://easylist-downloads.adblockplus.org/easylist-cookie.txt"
    key: str = "cookies"


class EasylistGermany(MetadataBase):
    url: str = "https://easylist.to/easylistgermany/easylistgermany.txt"
    key: str = "easylist_germany"


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


class EasylistGermanyAdservers(MetadataBase):
    urls: list = [
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
    key: str = "easylistgermany_adservers"

    def _download_tag_list(self):
        complete_tag_list = []
        for url in self.urls:
            self.url = url
            super()._download_tag_list()
            complete_tag_list.append(self.tag_list)


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
