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

                print("header items:, ", website_data.headers[tag])
                print("expected_value: ,", expected_value)
                for idx, element in expected_value.items():
                    print("idx:", idx, element, len(element))
                    expected_value.update(
                        {
                            int(idx): [
                                self._work_text(value) for value in element
                            ]
                        }
                    )

                print("header_value: ,", header_value)
                print("expected_value: ,", expected_value)

                header_value = [
                    val.replace(",", ";").split(";") for val in header_value
                ]
                header_value = [el for val in header_value for el in val]
                print("header_value2: ,", header_value)

                found_values = 0
                for key, value in expected_value.items():
                    found_val = False
                    for val in value:
                        if val in header_value:
                            found_val = True

                    found_values += int(found_val)

                print(f"found_values, {found_values}")

                if found_values == len(expected_value.keys()):
                    values.append(tag)

        return {VALUES: values}

    def _decide(self, website_data: WebsiteData) -> tuple[bool, float]:
        probability = len(website_data.values) / len(self.tags.keys())
        decision = probability >= self.decision_threshold
        return decision, probability
