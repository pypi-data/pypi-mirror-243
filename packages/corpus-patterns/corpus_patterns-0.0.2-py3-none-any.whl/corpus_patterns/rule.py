from pathlib import Path
from typing import Any, Self

import srsly  # type: ignore
from pydantic import BaseModel, StringConstraints, model_serializer
from typing_extensions import Annotated

from .ent_patterns_case import create_vs_patterns, party_styles
from .ent_patterns_item import create_item_patterns
from .patterns_date import patterns_date
from .patterns_docket import patterns_docket
from .patterns_generic import patterns_generic, patterns_generic_rules
from .patterns_juridical import patterns_juridical
from .patterns_report import patterns_report
from .patterns_statute import patterns_statute
from .patterns_unit import patterns_unit
from .utils import uncamel


class Rule(BaseModel):
    """`patterns` associated with a single `label` (optionally
    with an `id` as well that serve as the `ent_id_` in `spacy.tokens.Doc.ents`).
    It can also be used for pattern objects for `spacy.tokens.Doc.spans`. See generally:

    1. https://spacy.io/usage/rule-based-matching#entityruler-files
    2. https://spacy.io/usage/rule-based-matching#spanruler-files

    A `Rule` enables the creation of such pattern objects containing the same `Label`
    and custom `id`, if provided. Sample rule:

    ```py
    sample = Rule(
        id="ministry-labor",
        label="GOVT",
        patterns=[
            [
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "ministry"},
                {"LOWER": "of"},
                {"LOWER": "labor"},
            ]
        ],
    )
    ```
    """

    id: str | None = None
    label: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            to_upper=True,
            pattern=r"^[A-Za-z]+$",
        ),
    ]
    patterns: list[list[dict[str, Any]]]

    def __str__(self) -> str:
        return f"<Rule {self.ent_id})>"

    def __repr__(self) -> str:
        return f"<Rule {self.ent_id}: {len(self.patterns)} patterns>"

    @property
    def ent_id(self):
        return self.id or "-".join(uncamel(self.label)).lower()

    @model_serializer
    def ser_model(self) -> list[dict[str, Any]]:
        """Following the pydantic convention for .model_dump(); instead of a traditional
        `dict` return, the function results in a serialized list of patterns
        for consumption by either `create_file()` or the _entity_ruler_ spacy pipeline.
        """
        return [
            {"id": self.ent_id, "label": self.label.upper(), "pattern": pattern}
            for pattern in self.patterns
        ]

    @classmethod
    def setup(
        cls, label: str, patterns: list[list[dict[str, Any]]], id: str | None = None
    ) -> Self:
        return cls(id=id, label=label.lower(), patterns=patterns)


dates = Rule.setup(label="DATE", patterns=patterns_date)
jurs = Rule.setup(label="JUR", patterns=patterns_juridical)

statutes = Rule.setup(
    id="base-statute",
    label="STATUTE",
    patterns=patterns_statute,
)
generic_statutes = Rule.setup(
    id="generic-statute",
    label="STATUTE",
    patterns=patterns_generic_rules,
)
units = Rule.setup(label="UNIT", patterns=patterns_unit)

dockets = Rule.setup(label="DOCKET", patterns=patterns_docket)
generic = Rule.setup(label="GENERIC", patterns=patterns_generic)
reports = Rule.setup(label="REPORT", patterns=patterns_report)

options = [
    {"ENT_TYPE": {"IN": ["ORG", "PERSON", "JUR", "NAT"]}, "OP": "+"},
    {"POS": {"IN": ["PROPN", "ADP", "DET", "CCONJ"]}, "OP": "+"},
]
# should only be used after entities have already been created and the tagger is
# made part of the pipeline
cases = Rule.setup(
    label="CASE", patterns=create_vs_patterns(parties=party_styles + options)
)
items = Rule.setup(
    label="ITEM",
    patterns=list(
        create_item_patterns(
            unit_label="ITEM",
            container_labels=["STATUTE", "DOCKET", "GENERIC"],
        )
    ),
)
rules = [
    dates,
    jurs,
    dockets,
    reports,
    generic,
    statutes,
    generic_statutes,
    units,
    cases,  # entity combinations for span groups
    items,  # entity combinations for span groups
]


def create_rules(folder: Path):
    for rule in rules:
        target = folder.joinpath(f"{rule.ent_id}.jsonl")
        srsly.write_jsonl(path=target, lines=rule.model_dump())
