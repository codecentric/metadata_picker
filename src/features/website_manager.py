import json
from dataclasses import dataclass, field


@dataclass
class WebsiteData:
    html: str = field(default_factory=str)
    values: list = field(default_factory=list)
    headers: dict = field(default_factory=dict)
    raw_header: str = field(default_factory=str)


class Singleton:
    _instance = None

    def __init__(self, cls):
        self._class = cls

    def get_instance(self):
        if self._instance is None:
            self._instance = self._class()
        return self._instance

    def __call__(self):
        raise TypeError(
            "Singletons must only be accessed through `get_instance()`."
        )

    def __instancecheck__(self, inst):
        return isinstance(inst, self._class)


@Singleton
class WebsiteManager:
    website_data: WebsiteData

    def __init__(self):
        super().__init__()

        self.website_data = WebsiteData()

    def load_raw_data(
        self,
        html_content: str = "",
        raw_header: str = "",
        headers: dict = None,
    ) -> None:
        if headers is None:
            headers = {}

        if self.website_data.headers == {}:
            self.website_data.headers = headers

        if self.website_data.raw_header == "":
            self.website_data.raw_header = raw_header

        if raw_header != "":
            self._preprocess_header()

        if html_content != "" and self.website_data.html == "":
            self.website_data.html = html_content

    def _preprocess_header(self) -> None:
        header: str = self.website_data.raw_header
        header = (
            header.replace("b'", '"')
            .replace("/'", '"')
            .replace("'", '"')
            .replace('""', '"')
            .replace('/"', "/")
        )

        idx = header.find('b"')
        if idx >= 0 and header[idx - 1] == "[":
            bracket_idx = header[idx:].find("]")
            header = (
                header[:idx]
                + '"'
                + header[idx + 2 : idx + bracket_idx - 2].replace('"', " ")
                + header[idx + bracket_idx - 1 :]
            )

        header = json.loads(header)
        self.website_data.headers = header

    def reset(self) -> None:
        """
        Since the manager works on many websites consecutively, the website manager needs to be reset.

        """
        self.website_data = WebsiteData()
