from collections.abc import Iterator
from enum import Enum
from typing import Any

from .build_digits import DigitLists, PreUnit
from .utils import create_regex_options, spacy_in, spacy_re


class SerialUnit(Enum):
    """A statute's text is divided into (sometimes hierarchical) provisions.
    This structure combines both the adjective division, e.g. `Sec.`, `Section`, `Bk.`,
    etc. (which may have different casing and abbreviations) with presumed valid serial
    numbers, e.g. `1`, `1-b`, `III`, etc.
    """

    abbreviated_Sec1 = list(PreUnit.set_abbvs())
    abbreviated_sec1 = list(PreUnit.set_abbvs(cased="lower"))
    abbreviated_SEC1 = list(PreUnit.set_abbvs(cased="upper"))
    Section1 = list(PreUnit.set_fulls())
    section1 = list(PreUnit.set_fulls(cased="lower"))
    SECTION1 = list(PreUnit.set_fulls(cased="upper"))

    @classmethod
    def generate(
        cls, terminal_node: dict = {"IS_DIGIT": True}
    ) -> Iterator[list[dict[str, Any]]]:
        digits = spacy_re(create_regex_options(texts=DigitLists.generate_options()))
        for member in cls:
            for end in [terminal_node, digits]:
                start = [spacy_in(["of", "the", ",", "and", "&"], op="*")]
                if member.name.startswith("abbreviated_"):
                    yield start + [spacy_in(member.value), {"ORTH": "."}, end]
                    yield start + [spacy_in([f"{v}." for v in member.value]), end]
                yield start + [spacy_in(member.value), end]


special_clauses: list[dict[str, Any]] = [
    {"ENT_TYPE": "ORDINAL"},
    {"LOWER": {"IN": ["whereas"]}},
    {"LOWER": {"IN": ["clause", "clauses"]}},
]

patterns_unit = list(SerialUnit.generate()) + [special_clauses]
