PAIRS = [("(", ")"), ("[", "]")]


def customize_prefix_list(pfx: list[str] = ["\\(", "\\["]):
    """Only use prefix `(` and `[` if _not_ followed by a single word `\\w+`
    with a closing `)` or `]`

    Note that modifications to a prefix should be done after the prefix removed, e.g.
    if the prefix is `(`, modify the `(`<add here> when appending a new rule.
    This is because of `compile_suffix_regex` which appends a `^` at the start of
    every prefix.

    The opening `open` will be considered a prefix only if not subsequently terminated
    by a closing `close`.

    example | status of `(`
    --:|:--
    `(`Juan de la Cruz v. Example) | is prefix
    Juan `(`de) la Cruz v. Example | is _not_ prefix

    How to use:

    ```
    from spacy.tokenizer import Tokenizer
    from spacy.util import compile_prefix_regex

    default_prefixes = list(nlp.Defaults.prefixes)
    p = compile_prefix_regex(customize_prefix_list(default_prefixes))
    Tokenizer(
        nlp.vocab,
        prefix_search=p.search,
    )
    ```
    """
    for opened, closed in PAIRS:
        pfx.remove(f"\\{opened}")
        pfx.append(f"\\{opened}(?![\\w\\.]+\\{closed})")
    return pfx


def customize_suffix_list(sfx: list[str] = ["\\)", "\\]"]):
    """Enable partner closing character, e.g. `)` or `]` to be excluded as a suffix
    if matched with an opening `(` or `[` within the range provided by `num`.

    Assuming a range of 20, this means 19 characters will be allowed:

    Let's exceed this range with 22, this results in a split of the
    terminal character `)`:

    ```py
    text = "twenty_two_char_string"
    len(text)  # 22
    nlp.tokenizer.explain("A (twenty_two_char_string)")
    # [('TOKEN', 'A'),
    # ('PREFIX', '('),
    # ('TOKEN', 'twenty_two_char_string'),
    # ('SUFFIX', ')')]
    ```

    This becomes the exception to the general rule that the closing suffix `)` should
    be removed from the custom tokenizer.

    However, if the number of characters within a closed / covered single world is 19
    and below:

    ```py
    text = "smol"
    len(text)  # 4
    nlp.tokenizer.explain("A (smol)")
    # [('TOKEN', 'A'),
    # ('TOKEN', '(smol)'),
    # ('TOKEN', 'word')]
    ```

    The suffix ")" is removed per the general rule.

    How to use:

    ```
    from spacy.tokenizer import Tokenizer
    from spacy.util import compile_suffix_regex

    default_suffixes = list(nlp.Defaults.suffixes)
    s = compile_suffix_regex(compile_suffix_regex(default_suffixes))
    Tokenizer(
        nlp.vocab,
        suffix_search=s.search,
    )
    ```
    """

    for opened, closed in PAIRS:
        sfx.remove(f"\\{closed}")
        _pre = "".join([f"(?<!\\{opened}\\w{{{i}}})" for i in range(1, 20)])
        sfx.append(f"{_pre}\\{closed}")
    return sfx
