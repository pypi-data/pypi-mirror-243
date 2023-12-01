__version__ = "0.0.1"
from enum import Enum

from .ent_patterns_case import create_vs_patterns, party_styles
from .ent_patterns_item import create_item_patterns
from .patterns_date import patterns_date
from .patterns_docket import patterns_docket
from .patterns_generic import patterns_generic, patterns_generic_rules
from .patterns_juridical import patterns_juridical
from .patterns_report import patterns_report
from .patterns_statute import patterns_statute
from .patterns_unit import patterns_unit
from .rule import Rule, create_rules
from .tokens import set_tokenizer
from .tokens_infix import INFIXES_OVERRIDE
from .tokens_sfxpfx import customize_prefix_list, customize_suffix_list
from .tokens_single import set_single_tokens
