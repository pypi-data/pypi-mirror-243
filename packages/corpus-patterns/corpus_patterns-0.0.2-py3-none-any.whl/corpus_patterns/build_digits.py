import itertools
import string
from collections.abc import Iterator
from enum import Enum
from typing import Any

import inflect
import roman  # type: ignore

from .build_abbreviations import Abbv, Def
from .utils import spacy_re


class PreUnit(Enum):
    """A Unit of a statute may be abbreviated and the same may have different
    variations: e.g. titlecase, lowercase, and uppercase."""

    Title = Def(title="Title", abbv="Tit")
    SubT0 = Def(title="Subtitle")
    SubT1 = Def(title="SubTitle")
    SubT2 = Def(title="Sub-Title")
    Book = Def(title="Book", abbv="Bk")
    Chapter = Def(title="Chapter", abbv="Ch")
    SubChap0 = Def(title="Subchapter")
    SubChap1 = Def(title="SubChapter")
    SubChap2 = Def(title="Sub-Chapter", abbv="Sub-Chap")
    Article = Def(title="Article", abbv="Art")
    SubArt0 = Def(title="Subarticle")
    SubArt1 = Def(title="SubArticle")
    SubArt2 = Def(title="Sub-Article", abbv="Sub-Art")
    Section = Def(title="Section", abbv="Sec")
    SubSec0 = Def(title="Subsection")
    SubSec1 = Def(title="SubSection")
    SubSec2 = Def(title="Sub-Section", abbv="Sub-Sec")
    Par = Def(title="Paragraph", abbv="Par")
    SubPar0 = Def(title="Subparagraph")
    SubPar1 = Def(title="SubParagraph")
    SubPar2 = Def(title="Sub-Paragraph", abbv="Sub-Par")
    ProvRule = Def(title="Rule")
    Canon = Def(title="Canon")

    @classmethod
    def make_attr_rules(cls) -> Iterator[dict[str, Any]]:
        """Each member can contain explicit rules so that "digit patterns"
        are paired with the "adjective patterns":

        first node (adjective) | second node (digit)
        :-- | --:
        The member option for Sec., Section, etc. | a "digit" pattern e.g. 1, 1(a)

        The list of patterns can then be applied as part of an attribute ruler
        https://spacy.io/usage/linguistic-features#mappings-exceptions so that
        the token in the second node, i.e. the digit, can be set with the attributes
        defined in `attributes_to_set`.
        """
        for member in cls:
            p = [[{"ORTH": o}, p] for p in PROV_DIGITS for o in member.value.options]
            yield {
                "index": 0,
                "patterns": p,
                "attrs": {"POS": "NOUN"},
            }
            yield {
                "index": 1,
                "patterns": p,
                "attrs": {"POS": "NUM", "LIKE_NUM": True, "IS_DIGIT": True},
            }

    @classmethod
    def set_abbvs(cls, cased: str | None = None):
        for member in cls:
            if v := member.value.abbv:
                yield Def.get_cased_value(v, cased)

    @classmethod
    def set_fulls(cls, cased: str | None = None):
        for member in cls:
            yield Def.get_cased_value(member.value.title, cased)


org_options = set(
    op
    for s in (Abbv.Company, Abbv.Corporation, Abbv.Limited, Abbv.Incorporated)
    for op in s.value.options
)
ph_options = set(op for s in (Abbv.Phil1, Abbv.Phil2) for op in s.value.options)


p = inflect.engine()

roman_upper = [roman.toRoman(i) for i in range(1, 100)]
a_z_lower = [i for i in string.ascii_lowercase]
pairs = itertools.combinations_with_replacement(a_z_lower, r=2)
aa_zz_lower = [f"{a}{b}" for a, b in pairs]


class DigitLists(Enum):
    HundredDigit = [str(i) for i in range(0, 100)]
    WordHundredDigit = [p.number_to_words(num=i) for i in range(1, 100)]  # type: ignore
    RomanHundredLower = [i.lower() for i in roman_upper]
    RomanHundredUpper = [roman.toRoman(i) for i in range(1, 100)]
    AtoZSingleLower = a_z_lower
    AtoZSingleUpper = [i.upper() for i in a_z_lower]
    AtoZDoubleLower = aa_zz_lower
    AtoZDoubleUpper = [i.upper() for i in aa_zz_lower]

    @classmethod
    def generate_options(cls) -> list[str]:
        options: list[str] = []
        for member in cls:
            options.extend(member.value)  # type: ignore
        return options


HAS_DIGIT = spacy_re(v=".*\\d.*")
"""Any token containing a digit should be used in tandem with an attribute ruler."""

DOTTED = spacy_re(v="(\\d\\.)+\\d?")

IS_COVERED = spacy_re(v=".*\\(\\w{1,2}\\).*")
"""Any token containing a digit should be used in tandem with an attribute ruler."""

SPECIFIC = spacy_re("(" + "|".join(DigitLists.generate_options()) + ")")
"""Any token matching the options created by DigitLists"""

IS_ROMAN = spacy_re(v="[IXV]+[-\\.][A-Z]{1,2}")
"""Handle combinations like I-A"""

PROV_DIGITS = [SPECIFIC, HAS_DIGIT, IS_COVERED, IS_ROMAN, DOTTED]
