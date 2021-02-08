from features.metadata_base import MetadataBase
from features.website_manager import WebsiteData
from lib.constants import VALUES


class Security(MetadataBase):
    decision_threshold = 1

    tags: dict = {
        "x-content-type-options": {
            "nosniff",
        },
        "x-frame-options": {"same_origin"},
        "content-security-policy": {
            "same_origin",
        },
        "x-xss-protection": {
            "1",
            "mode=block",
        },
    }

    @staticmethod
    def _work_text(text: str) -> str:
        return text.replace("_", "").replace("-", "").lower()

    def _start(self, website_data: WebsiteData) -> dict:
        values = []

        for tag, expected_value in self.tags.items():
            if tag in website_data.headers:

                header_value = [
                    self._work_text(value)
                    for value in website_data.headers[tag]
                ]
                expected_value = {
                    self._work_text(value) for value in expected_value
                }

                if (set(expected_value) & set(header_value)) == set(
                    expected_value
                ):
                    values.append(tag)

        return {VALUES: values}

    def _decide(self, website_data: WebsiteData) -> tuple[bool, float]:
        probability = len(website_data.values) / len(self.tags.keys())
        decision = probability >= self.decision_threshold
        return decision, probability
