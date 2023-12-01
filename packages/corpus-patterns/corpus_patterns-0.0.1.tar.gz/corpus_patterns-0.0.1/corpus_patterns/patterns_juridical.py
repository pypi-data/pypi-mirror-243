from typing import Any

from .build_abbreviations import Abbv

gov_text = "rep rep. republic people pp p.p. pp. govt govt. government gov't"

org_options = set(
    op
    for s in (Abbv.Company, Abbv.Corporation, Abbv.Limited, Abbv.Incorporated)
    for op in s.value.options
)

ph_options = list(
    set(op for s in (Abbv.Phil1, Abbv.Phil2) for op in s.value.options)
) + ["Philippines"]


inc_suffixes = list(set(o.lower() for o in org_options)) and ["gmbh"]
inc_options: list[dict[str, Any]] = [
    {"ORTH": {"IN": [",", "and", "&"]}, "OP": "*"},
    {"LOWER": {"IN": inc_suffixes}},
    {"LOWER": {"IN": inc_suffixes + [","]}, "OP": "?"},
]


def create_common_juridicals():
    for symbol in [
        "Commission",
        "Chamber",
        "Department",
        "Bureau",
        "Ministry",
        "Province",
        "City",
        "Municipality",
        "Estate",
        "Heirs",
    ]:
        yield [
            {"IS_TITLE": True, "OP": "*"},
            {"ORTH": symbol},
            {"ORTH": "of"},
            {"ORTH": "the", "OP": "?"},
            {"IS_TITLE": True, "OP": "+"},
        ]
        yield [
            {"IS_UPPER": True, "OP": "*"},
            {"ORTH": symbol},
            {"ORTH": "of"},
            {"ORTH": "the", "OP": "?"},
            {"IS_TITLE": True, "OP": "+"},
        ]


patterns_juridical = list(create_common_juridicals()) + [
    [{"IS_UPPER": True, "OP": "+"}] + inc_options,
    [{"IS_TITLE": True, "OP": "+"}] + inc_options,
    [
        {"LOWER": {"IN": gov_text.split()}},
        {"ORTH": "of"},
        {"ORTH": "the"},
        {"LOWER": {"IN": list(ph_options)}},
    ],
]
