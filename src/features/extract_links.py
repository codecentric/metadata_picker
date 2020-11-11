import os

from bs4 import BeautifulSoup

from features.metadata_base import MetadataBase
from features.website_manager import WebsiteData
from lib.constants import VALUES


class ExtractLinks(MetadataBase):
    key: str = "extracted_links"

    # Based on: https://www.file-extensions.org/filetype/extension/name/dangerous-malicious-files
    #           https://www.howtogeek.com/137270/50-file-extensions-that-are-potentially-dangerous-on-windows/
    #           https://sensorstechforum.com/file-types-used-malware-2019/
    #           https://www.howtogeek.com/127154/how-hackers-can-disguise-malicious-programs-with-fake-file-extensions/
    malicious_extensions = [
        "msp",
        "cfxxe",
        "php3",
        "vb",
        "vb",
        "swf",
        "mcq",
        "dyv",
        "html",
        "ps1",
        "jar",
        "9",
        "ocx",
        "chm",
        "mshxml",
        "vbs",
        "hta",
        "lkh",
        "hlp",
        "iws",
        "gadget",
        "pr",
        "wlpginstall",
        "kcd",
        "docx",
        "dom",
        "hsq",
        "aepl",
        "0_full_0_tgod_signed",
        "dyz",
        "psc1",
        "py",
        "cyw",
        "blf",
        "osa",
        "pdf",
        "shs",
        "xlm",
        "exe_renamed",
        "bat",
        "dll",
        "exe1",
        "pif",
        "xir",
        "vbs",
        "qrn",
        "mjg",
        "fag",
        "xdu",
        "xlam",
        "com",
        "ps2xml",
        "reg",
        "cpl",
        "plc",
        "ska",
        "xlv",
        "bmw",
        "msc",
        "tko",
        "rna",
        "msh2xml",
        "wmf",
        "hlw",
        "uzy",
        "nls",
        "inf",
        "iva",
        "zix",
        "gzquar",
        "cxq",
        "ppam",
        "bps",
        "ppt",
        "dxz",
        "ezt",
        "jse",
        "xnxx",
        "xls",
        "exe",
        "aru",
        "lok",
        "hta",
        "vba",
        "xltm",
        "atm",
        "xtbl",
        "txs",
        "xlsm",
        "mjz",
        "mfu",
        "wsf",
        "cih",
        "xnt",
        "capxml",
        "docm",
        "sfx",
        "fjl",
        "cmd",
        "msh",
        "aut",
        "ws",
        "tti",
        "dlb",
        "msh1",
        "ozd",
        "fuj",
        "exe",
        "class",
        "386",
        "qit",
        "ps2",
        "delf",
        "cla",
        "ps1xml",
        "bkd",
        "doc",
        "bin",
        "dev",
        "cc",
        "sys",
        "dx",
        "vbx",
        "bup",
        "vxd",
        "rsc_tmp",
        "js",
        "spam",
        "tps",
        "htm",
        "wsh",
        "bll",
        "sop",
        "wsc",
        "bxz",
        "jar",
        "tsa",
        "msi",
        "pcx",
        "vbe",
        "smm",
        "rhk",
        "dli",
        "application",
        "let",
        "pid",
        "upa",
        "msh1xml",
        "ce0",
        "psc2",
        "msh2",
        "lpaq5",
        "ctbl",
        "boo",
        "js",
        "buk",
        "hts",
        "sldm",
        "bat",
        "smtmp",
        "dllx",
        "ppsm",
        "docm",
        "bhx",
        "scf",
        "fnr",
        "pptm",
        "drv",
        "doc",
        "vzr",
        "ssy",
        "scr",
        "dotm",
        "s7p",
        "ceo",
        "tmp",
        "lik",
        "lnk",
        "pgm",
        "dll",
        "oar",
        "bqf",
        "zvz",
        "dbd",
        "vexe",
        "potm",
        "\u202e",
    ]

    @staticmethod
    def __extract_extensions(links: list):
        file_extensions = [os.path.splitext(link)[-1] for link in links]
        file_extensions = [x for x in list(set(file_extensions)) if x != ""]
        return file_extensions

    @staticmethod
    def __extract_images(soup: BeautifulSoup) -> list:
        # TODO: We only gather the url here. There is more information stored here!
        image_links = [image.attrs.get("src") for image in soup.findAll("img")]
        return image_links

    def __extract_malicious_extensions(self, extensions: list) -> list:
        return [
            extension
            for extension in extensions
            if extension.replace(".", "") in self.malicious_extensions
        ]

    def _start(self, website_data: WebsiteData) -> dict:
        soup = self._create_html_soup(website_data.html)

        raw_links = self._extract_raw_links(soup)
        image_links = self.__extract_images(soup)
        extensions = self.__extract_extensions(raw_links)
        malicious_extensions = self.__extract_malicious_extensions(extensions)

        return {
            VALUES: raw_links,
            "images": image_links,
            "extensions": extensions,
            "malicious_extensions": malicious_extensions,
        }
