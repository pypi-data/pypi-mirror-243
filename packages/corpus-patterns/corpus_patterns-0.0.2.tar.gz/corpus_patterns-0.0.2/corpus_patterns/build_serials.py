from typing import Any, NamedTuple

from .utils import set_optional_node, spacy_in, spacy_re


class Duo(NamedTuple):
    """Given two letters, create possible patterns using uppercase text."""

    a: str
    b: str

    @property
    def x(self):
        return self.a.upper()

    @property
    def y(self):
        return self.b.upper()

    @property
    def as_token(self) -> dict[str, list[dict[str, str]]]:
        """Used to create special rules for custom tokenizer."""
        return {f"{self.x}.{self.y}.": [{"ORTH": f"{self.x}.{self.y}."}]}

    @property
    def v1(self) -> list[dict[str, str]]:
        # R . A .
        return [{"ORTH": self.x}, {"ORTH": "."}, {"ORTH": self.y}, {"ORTH": "."}]

    @property
    def v2(self) -> list[dict[str, str]]:
        return [{"ORTH": f"{self.x}."}, {"ORTH": f"{self.y}."}]  # R. A.

    @property
    def v3(self) -> list[dict[str, str]]:
        return [{"ORTH": f"{self.x}.{self.y}."}]  # R.A.

    @property
    def v4(self) -> list[dict[str, str]]:
        return [{"ORTH": f"{self.x}{self.y}"}]  # RA

    @property
    def patterns(self) -> list[list[dict[str, str]]]:
        return [self.v1, self.v2, self.v3, self.v4]

    def add_to_each_pattern(self, terminators: list[dict[str, Any]]):
        for p in self.patterns:
            yield p + terminators


class Serial(NamedTuple):
    """A `Serial` refers to:

    1. possible two-letter acronym (`duo`) and/or
    2. word `variants`

    If no `duo` exists, will only create word patterns using `variants`.
    """

    variants: list[str] = []
    duo: str | None = None
    pre: list[str] = ["no", "nos", "no.", "nos."]
    regex: str = "[A-Z\\d\\-\\.]*\\d[A-Z\\d\\-\\.]*"

    @property
    def target(self) -> list[dict[str, Any]]:
        return [
            set_optional_node(),  # often found here Republic Act (RA) No. 8294
            spacy_in(self.pre, default="LOWER"),
            set_optional_node(),  # sometimes found here Republic Act No. (RA) 8294
            spacy_re(self.regex),
        ]

    @property
    def token_parts(self):
        """The first pass is for indiscriminate words e.g. `bar matter`; the second, for
        dealing with periods, e.g. `adm. matter`. The first will generate the following
        as token parts ('bar','matter'); the second: ('adm.','matter'),
        ('adm','.','matter')
        """
        objs = set()
        for words in self.variants:
            partial = []
            for word in words.split():
                partial.append(word)
            objs.add(tuple(partial))
        for words in self.variants:
            partial = []
            for word in words.split():
                if word.endswith("."):
                    cleaned = word.removesuffix(".")
                    partial.append(cleaned)
                    partial.append(".")
                else:
                    partial.append(word)
            objs.add(tuple(partial))
        return objs

    @property
    def title_cased_pre_words(self) -> list[list[dict[str, Any]]]:
        """R.A"""
        return [
            [{"ORTH": sub.title()} for sub in subtokens] + self.target
            for subtokens in self.token_parts
        ]

    @property
    def upper_cased_pre_words(self) -> list[list[dict[str, Any]]]:
        return [
            [{"ORTH": sub.upper()} for sub in subtokens] + self.target
            for subtokens in self.token_parts
        ]

    @property
    def title_cased_unpre_words(self) -> list[list[dict[str, Any]]]:
        return [
            [{"ORTH": sub.title()} for sub in subtokens] + [spacy_re(self.regex)]
            for subtokens in self.token_parts
        ]

    @property
    def upper_cased_unpre_words(self) -> list[list[dict[str, Any]]]:
        return [
            [{"ORTH": sub.upper()} for sub in subtokens] + [spacy_re(self.regex)]
            for subtokens in self.token_parts
        ]

    @property
    def initials(self) -> Duo | None:
        if not self.duo:
            return None
        if len(self.duo) != 2:
            return None
        return Duo(a=self.duo[0], b=self.duo[1])

    @property
    def word_patterns(self) -> list[list[dict[str, Any]]]:
        patterns = []
        patterns.extend(self.title_cased_pre_words)
        patterns.extend(self.upper_cased_pre_words)
        patterns.extend(self.title_cased_unpre_words)
        patterns.extend(self.upper_cased_unpre_words)
        return patterns

    @property
    def letter_patterns(self) -> list[list[dict[str, Any]]]:
        items: list[list[dict[str, Any]]] = []
        if not self.initials:
            return items
        for target_nodes in (
            self.target,
            [spacy_re(self.regex)],
        ):
            for b in self.initials.add_to_each_pattern(target_nodes):
                items.append(b)
        return items

    @property
    def patterns(self) -> list[list[dict[str, Any]]]:
        words = self.word_patterns
        letters = self.letter_patterns
        return words + letters if letters else words
