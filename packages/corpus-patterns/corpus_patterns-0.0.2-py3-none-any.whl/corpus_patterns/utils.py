import re
from collections.abc import Iterable
from typing import Any

from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

camel_case_pattern = re.compile(
    r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)"
)


def uncamel(text: str) -> list[str]:
    """For text in camelCaseFormatting, convert into a list of strings."""
    return [m.group(0) for m in camel_case_pattern.finditer(text)]


def check_titlecased_word(v: str) -> str:
    assert all(bit.istitle for bit in v.split("-")), f"{v} is not titlecased."
    return v


TitledString = Annotated[str, AfterValidator(check_titlecased_word)]


def create_regex_options(texts: Iterable[str]):
    return "(" + "|".join(texts) + ")"


def spacy_re(v: str, anchored: bool = True, op: str | None = None) -> dict[str, Any]:
    """Helper function to add an anchored, i.e. `^`<insert value `v` here>`$`
    regex pattern, following `{"TEXT": {"REGEX": f"^{v}$"}}` spacy convention,
    unless modified by arguments.
    """
    if anchored:
        v = f"^{v}$"
    result = {"TEXT": {"REGEX": v}}
    return result | {"OP": op} if op else result


def spacy_in(v_list: list[str], default: str = "ORTH", op: str | None = None):
    """Helper function to add a specific list of options following
    `{"ORTH": {"IN": v_list}}` spacy convention, unless modified by arguments.
    """
    result = {default: {"IN": v_list}}
    return result | {"OP": op} if op else result


def set_optional_node():
    """Deal with nodes like (R.A.), [PD]"""
    _open = create_regex_options(texts=("\\(", "\\["))
    _close = create_regex_options(texts=("\\)", "\\]"))
    _in = "[\\w\\.]+"
    regex = "".join([_open, _in, _close])
    return spacy_re(v=regex, op="?")
