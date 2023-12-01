from spacy.language import Language
from spacy.tokenizer import Tokenizer  # type: ignore
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

from .tokens_infix import INFIXES_OVERRIDE
from .tokens_sfxpfx import customize_prefix_list, customize_suffix_list
from .tokens_single import set_single_tokens


def set_tokenizer(nlp: Language) -> Tokenizer:
    infix_re = compile_infix_regex(INFIXES_OVERRIDE)

    sfx_override = customize_suffix_list(list(nlp.Defaults.suffixes))  # type: ignore
    suffix_re = compile_suffix_regex(sfx_override)

    pfx_override = customize_prefix_list(list(nlp.Defaults.prefixes))  # type: ignore
    prefix_re = compile_prefix_regex(pfx_override)

    return Tokenizer(
        nlp.vocab,
        rules=set_single_tokens(),
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
    )
