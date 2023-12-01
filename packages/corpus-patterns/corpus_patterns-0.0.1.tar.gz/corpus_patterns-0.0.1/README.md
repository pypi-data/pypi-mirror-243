# corpus-patterns

![Github CI](https://github.com/justmars/corpus-patterns/actions/workflows/main.yml/badge.svg)

## Create a custom tokenizer

```py
from corpus_patterns import set_tokenizer

nlp = spacy.blank("en")
nlp.tokenizer = set_tokenizer(nlp)
```

The tokenizer:

1. Removes dashes from infixes
2. Adds prefix/suffix rules for parenthesis/brackets
3. Adds special exceptions to treat dotted text as a single token

## Add .jsonl files to directory

Each file will contain lines of spacy matcher patterns.

```py
from corpus_patterns import create_rules
from pathlib import Path

create_rules(folder=Path(Path("location-here")))  # check directory
```
