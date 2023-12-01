from typing import Any

from .build_abbreviations import Abbv
from .utils import create_regex_options, spacy_in, spacy_re

months = [
    month
    for defined_month in (
        Abbv.January,
        Abbv.February,
        Abbv.March,
        Abbv.April,
        Abbv.May,
        Abbv.June,
        Abbv.July,
        Abbv.August,
        Abbv.Sept1,
        Abbv.Sept2,
        Abbv.October,
        Abbv.November,
        Abbv.December,
    )
    for month in defined_month.value.options
]

days = spacy_in([f"{str(i)}" for i in range(1, 32)] + [f"0{i}" for i in range(1, 10)])

ranged_years = create_regex_options(["(19\\d{2})", "(20\\d{2})"])

optional_predate_indicators: list[dict[str, Any]] = [
    {"ORTH": ",", "OP": "?"},
    {"ORTH": {"IN": ["dated", "promulgated", "issued"]}, "OP": "?"},
    {"ORTH": "on", "OP": "?"},
]

date_us: list[list[dict[str, Any]]] = [
    optional_predate_indicators
    + [
        {"ORTH": month_name},
        days,
        {"ORTH": ",", "OP": "?"},
        spacy_re(ranged_years),
    ]
    for month_name in months  # , Feb. 01, 2023; dated Jan. 1, 2000
]

date_uk: list[list[dict[str, Any]]] = [
    optional_predate_indicators
    + [
        days,
        {"ORTH": month_name},
        {"ORTH": ",", "OP": "?"},
        spacy_re(ranged_years),
    ]
    for month_name in months  # 01 Feb 2023; dated 01 Jan. 2000
]


covered_parent_year: list[dict[str, Any]] = [
    spacy_re("\\(" + ranged_years + "\\)"),  # (2023)
]


covered_bracket_year: list[dict[str, Any]] = [
    spacy_re("\\[" + ranged_years + "\\]"),  # [2023]
]

series_year: list[dict[str, Any]] = [
    {"ORTH": ",", "OP": "?"},
    {"LOWER": {"IN": ["s.", "series"]}},  # , s. of 2023
    {"ORTH": "of", "OP": "?"},
    spacy_re(ranged_years),
]

patterns_date = (
    date_us + date_uk + [covered_parent_year, covered_bracket_year, series_year]
)
