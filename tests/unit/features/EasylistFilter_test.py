from features.EasylistFilter import EasyFilter


def _create_sample_easylist() -> list:
    easylist = [
        "! *** easylist:easylist/easylist_general_block.txt ***",
        r"/adv_horiz.",
        r"@@||imx.to/dropzone.js$script",
        r"||testimx.to/dropzone.js$script",
    ]

    return easylist


def _create_sample_urls() -> list:
    urls = [
        "https://www.dictionary.com/",
        "/adv_horiz.",
        "imx.to/dropzone.js",
        "testimx.to/dropzone.js",
    ]
    return urls


"""
--------------------------------------------------------------------------------
"""


def test_easylist_filter():
    urls = _create_sample_urls()
    easylist = _create_sample_easylist()

    found_matches = []

    for url in urls:
        adblock_filter = EasyFilter(easylist)
        found_matches += adblock_filter.match(url)

    print(found_matches)
    assert "/adv_horiz." in found_matches
    assert "@@||imx.to/dropzone.js$script" not in found_matches
    # assert "testimx.to/dropzone.js" in found_matches


"""
--------------------------------------------------------------------------------
"""
