from features.metadata_base import MetadataBase
from features.website_manager import WebsiteData
from lib.constants import VALUES


class Security(MetadataBase):
    decision_threshold = 1

    tags = {
        "X-Content-Type-Options": "nosniff",
        "content-security-policy": "same_origin",
        "X-XSS-Protection": "1; mode=block",
    }

    def _start(self, website_data: WebsiteData) -> dict:
        values = []
        for tag, expected_value in self.tags.items():
            if (
                tag.lower() in website_data.headers
                and website_data.headers[tag.lower()] == expected_value
            ):
                values.append(tag)
        return {VALUES: values}

    def _decide(self, website_data: WebsiteData) -> tuple[bool, float]:
        probability = 0
        for tag in self.tags.keys():
            if tag in website_data.values:
                probability += 1.0 / len(self.tags.keys())

        decision = probability >= self.decision_threshold
        return decision, probability
