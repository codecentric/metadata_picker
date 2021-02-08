from features.metadata_base import MetadataBase
from features.website_manager import WebsiteData
from lib.constants import VALUES


class Security(MetadataBase):
    decision_threshold = 1

    tags: dict = {
        "x-content-type-options": {0: ["nosniff"]},
        "x-frame-options": {0: ["deny", "same_origin"]},
        "content-security-policy": {
            0: ["deny", "same_origin"],
        },
        "x-xss-protection": {
            0: ["1"],
            1: ["mode=block"],
        },
        "cache-control": {0: ["no-cache", "no-store"]},
        "strict-transport-security": {0: ["max-age=", "includeSubDomains"]},
    }

    @staticmethod
    def _work_text(text: str) -> str:
        return text.replace("_", "").replace("-", "").lower()

    def _start(self, website_data: WebsiteData) -> dict:
        values = []

        for tag, expected_value in self.tags.items():
            if tag in website_data.headers:
                header_value = [
                    self._work_text(value).replace(",", ";").split(";")
                    for value in website_data.headers[tag]
                ]
                header_value = [el for val in header_value for el in val]

                for idx, element in expected_value.items():
                    expected_value.update(
                        {
                            int(idx): [
                                self._work_text(value) for value in element
                            ]
                        }
                    )

                found_values = sum(
                    [
                        1
                        for value in expected_value.values()
                        for val in value
                        if val in header_value
                    ]
                )

                if tag == "strict-transport-security":
                    for el in header_value:
                        if (
                            el.startswith("maxage=")
                            and int(el.split("=")[-1]) > 0
                        ):
                            found_values += 1

                if found_values == len(expected_value.keys()):
                    values.append(tag)

        return {VALUES: values}

    def _decide(self, website_data: WebsiteData) -> tuple[bool, float]:
        probability = len(website_data.values) / len(self.tags.keys())
        decision = probability >= self.decision_threshold
        return decision, probability
