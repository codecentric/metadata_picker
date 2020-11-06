"""
Loosely based on https://github.com/atereshkin/abpy
"""

import re
from typing import Optional

URLS = ["https://www.dictionary.com/", "/adv_horiz."]

RE_TOK = re.compile(r"\W")

# TODO: Unclear what this does (Replace the left with the right, but why?
MAP_RE = (
    (r"\|\|", r"(//|\.)"),
    (r"\^", r"[/\\:+!@#\$^\^&\*\(\)\|]"),
    (r"\*", r".*"),
)


# TODO: Is this truly necessary?
class RuleSyntaxError(Exception):
    pass


# TODO: Unclear what this is for
TYPE_OPTS = (
    ("script", "external scripts loaded via HTML script tag"),
    ("image", "regular images, typically loaded via HTML img tag"),
    ("stylesheet", "external CSS stylesheet files"),
    ("object", "content handled by browser plugins, e.g. Flash or Java"),
    ("xmlhttprequest", "requests started by the XMLHttpRequest object"),
    ("object-subrequest", "requests started plugins like Flash"),
    ("subdocument", "embedded pages, usually included via HTML frames"),
    (
        "document",
        "the page itself (only exception rules can be applied to the page)",
    ),
    (
        "elemhide",
        "for exception rules only, "
        "similar to document but only disables element hiding rules on the page "
        "rather than all filter rules (Adblock Plus 1.2 and higher required)",
    ),
    ("other", "types of requests not covered in the list above"),
)
TYPE_OPT_IDS = [x[0] for x in TYPE_OPTS]


class EasylistRule:
    def __init__(self, rule):
        self.rule = rule.strip()

        if "$" in rule:
            try:
                self.pattern, self.optional = rule.split("$")
            except ValueError:
                raise RuleSyntaxError()
        else:
            self.pattern = self.rule
            self.optional = ""

        self.regex = self._to_regex()

        self.excluded_elements = []
        self.matched_elements = []

        for optional in self.optional.split(","):
            if optional.startswith("~") and optional[1:] in TYPE_OPT_IDS:
                self.excluded_elements.append(optional)
            elif optional in TYPE_OPT_IDS:
                self.matched_elements.append(optional)
        if not self.matched_elements:
            self.matched_elements = TYPE_OPT_IDS

    def get_tokens(self):
        return RE_TOK.split(self.pattern)

    def match(self, url):
        return self.regex.search(url)

    def _to_regex(self):
        re_str = re.escape(self.pattern)
        for m in MAP_RE:
            re_str = re_str.replace(*m)
        return re.compile(re_str)

    def __repr__(self):
        return self.rule


class EasyFilter:
    def __init__(self, easylist: list):
        self.comment = "!"
        self.index = {}

        for line in easylist:
            if not line.startswith(self.comment) and "##" not in line:
                rule = self._create_rule(line)
                if rule:
                    self._add_token_and_rule_to_index(rule)

    @staticmethod
    def _create_rule(line: str) -> Optional[EasylistRule]:
        rule = None
        try:
            rule = EasylistRule(line)
        except RuleSyntaxError:
            print("syntax error in ", line)
        return rule

    def _add_token_and_rule_to_index(self, rule):
        for tok in rule.get_tokens():
            if len(tok) > 2:
                if tok not in self.index:
                    self.index[tok] = []
                self.index[tok].append(rule)

    def match(self, url):
        matches = []
        for tok in RE_TOK.split(url):
            if len(tok) > 2 and tok in self.index:
                for rule in self.index[tok]:
                    if rule.match(url):
                        print(f"rule: {rule}")
                        matches.append(str(rule))
        return matches


# FIXME: Just for testing, remove prior to MERGE/PULL!
def main():
    with open("easylist.txt") as easylist_file:
        easylist = easylist_file.read()

    for url in URLS:
        easylist_splitted = easylist.split("\n")
        adblock_filter = EasyFilter(easylist_splitted)
        found_matches = adblock_filter.match(url)

        print(f"For url '{url}' found these matches: '{found_matches}'")


if __name__ == "__main__":
    main()
