from typing import Any

from .build_serials import Serial
from .utils import set_optional_node, spacy_in, spacy_re

ao = Serial(
    duo="ao",
    regex="\\d{1,4}(-?(A|B|C))?",
    variants=[
        "administrative order",
        "admin order",
        "adm. order",
    ],
)


rule_symbols = [
    "General Order",
    "Department Order",
    "Wage Order",
    "Memorandum Order",
    "Ministry Order",
    "Letter of Instruction",
    "Memorandum Circular",
    "Memo Circular",
    "Administrative Circular",
    "Department Circular",
    "Joint Department Circular",
    "Joint Circular",
    "City Resolution",
    "City Ordinance",
    "Municipal Resolution",
    "Municipal Ordinance",
    "Zoning Ordinance",
    "Policy Instruction",
    "Order",
    "Circular",
    "Resolution",
    "Ordinance",
    "Proclamation",
    "Regulation",
    "Memorandum",
]

generic_symbols = [
    "Civil Case",
    "Criminal Case",
    "Legal Opinion",
    "Case",
    "Opinion",
    "Decision",
]

excludes = [
    "vacate",
    "valid",
    "affirm",
    "affirms",
    "in",
    "under",
    "per",
    "remands",
    "re-opens",
    "reinstates",
    "void",
    "unlike",
    "until",
    "while",
    "with",
    "through",
    "that",
    "to",
    "accompanying",
    "since",
    "issues",
    "issued",
    "passes",
    "passed",
    "promulgates",
    "promulgated",
]

upper_opt_title_req = [
    {
        "IS_UPPER": True,
        "OP": "*",
        "LOWER": {"NOT_IN": excludes},
    },
    {
        "IS_TITLE": True,
        "OP": "+",
        "LOWER": {"NOT_IN": excludes},
    },
]


title_opt_upper_req = [
    {
        "IS_TITLE": True,
        "OP": "*",
        "LOWER": {"NOT_IN": excludes},
    },
    {
        "IS_UPPER": True,
        "OP": "+",
        "LOWER": {"NOT_IN": excludes},
    },
]


numbered_doc = [
    set_optional_node(),
    spacy_in(["no", "nos", "no.", "nos."], default="LOWER"),
    spacy_re("\\d[\\w-]+"),
]


def improve_ao():
    for pattern in ao.patterns:
        yield pattern
        yield upper_opt_title_req + pattern
        yield title_opt_upper_req + pattern


def create_generics(symbols: list[str]):
    for sym in symbols:
        words_req = [{"ORTH": word} for word in sym.split()]
        yield upper_opt_title_req + words_req + numbered_doc
        yield title_opt_upper_req + words_req + numbered_doc
        yield words_req + numbered_doc


def create_numbered():
    yield upper_opt_title_req + numbered_doc
    yield title_opt_upper_req + numbered_doc


patterns_generic_rules = list(create_generics(rule_symbols)) + list(improve_ao())

patterns_generic = list(create_generics(generic_symbols)) + list(create_numbered())
