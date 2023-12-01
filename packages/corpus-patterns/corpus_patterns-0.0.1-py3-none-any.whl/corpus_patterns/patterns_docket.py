import itertools
from typing import Any

from .build_serials import Serial
from .utils import spacy_in, spacy_re

general_register = Serial(duo="gr")

special_l: list[dict[str, Any]] = [
    {"TEXT": {"REGEX": "^L-\\d{4,}$", "NOT_IN": ["L-300"]}},
]
# prevent L-300 capture if not preceded by NUM

numbered_l: list[dict[str, Any]] = [
    spacy_in(["no", "nos", "no.", "nos."], default="LOWER"),
    spacy_re("L-\\d{4,}"),
]

cagrs: dict[str, Any] = spacy_in([  # type: ignore
    "CA-G.R.",
    "CA-GR",
    "CA-GR.",
    "CAG.R.",
    "CAGR.",
    "CA.GR.",
    "CAGR",
])


def create_ca_patterns():
    ca_letters: list[list[dict[str, str]]] = Serial(duo="ca").initials.patterns  # type: ignore
    gr_letters: list[list[dict[str, str]]] = Serial(duo="gr").initials.patterns  # type: ignore
    _patterns = [x + y for x, y in itertools.product(ca_letters, gr_letters)]
    _patterns.insert(0, [cagrs])
    for ptn in _patterns:
        yield ptn + [
            {"IS_UPPER": True, "OP": "*"},
            spacy_in(["no", "nos", "no.", "nos."], default="LOWER"),
            spacy_re("\\d[\\w-]+"),
        ]


bar_matter = Serial(
    duo="bm",
    variants=[
        "bar mat.",
        "bar matter",
    ],
)

admin_case = Serial(
    duo="ac",
    variants=[
        "adm case",
        "adm. case",
        "admin. case",
        "admin case",
        "administrative case",
    ],
)

ams = [
    "a.m.",
    "adm mat",
    "adm matter",
    "adm. mat.",
    "adm. mat",
    "adm. matter",
    "admin mat",
    "admin mat.",
    "admin. mat.",
    "admin. matter",
    "administrative matter",
]
ipis = ["oca ipi", "oca i.p.i."]
variant_ams = []
for am in ams:
    for ipi in ipis:
        variant_ams.append(f"{am} {ipi}")
ams = sorted(variant_ams + ipis, key=lambda x: len(x), reverse=True)
admin_matter = Serial(duo="am", variants=ams)


patterns_docket: list[list[dict[str, Any]]] = (
    list(create_ca_patterns())
    + general_register.patterns
    + [numbered_l, special_l]
    + admin_matter.patterns
    + admin_case.patterns
    + bar_matter.patterns
)
