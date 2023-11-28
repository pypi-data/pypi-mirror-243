import spacy
from spacy.lang.char_classes import (
    ALPHA,
    ALPHA_LOWER,
    ALPHA_UPPER,
    CONCAT_QUOTES,
    LIST_ELLIPSES,
    LIST_ICONS,
)

from lextok.rules.abbreviations import Abbv, Prov
from lextok.rules.rule_docketnums import DocketNum
from lextok.rules.rule_statutenums import StatuteNum

# Remove hyphen '-' as infix, see https://spacy.io/usage/linguistic-features#native-tokenizer-additions
INFIXES_OVERRIDE = (
    LIST_ELLIPSES
    + LIST_ICONS
    + [
        r"(?<=[0-9])[+\\-\\*^](?=[0-9-])",
        r"(?<=[{al}{q}])\\.(?=[{au}{q}])".format(
            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
        ),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        # ✅ Commented out regex that splits on hyphens between letters:
        # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
        r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
    ]
)

PAIRS = [("(", ")"), ("[", "]")]


def custom_prefix_list(nlp: spacy.language.Language):
    """Only use prefix `(` and `[` if _not_ followed by a single word `\\w+`
    with a closing `)` or `]`

    Note that modifications to a prefix should be done after the prefix removed, e.g.
    if the prefix is `(`, modify the `(`<add here> when appending a new rule.
    This is because of `compile_suffix_regex` which appends a `^` at the start of every prefix.

    The opening `open` will be considered a prefix only if not subsequently terminated by a closing `close`.

    example | status of `(`
    --:|:--
    `(`Juan de la Cruz v. Example) | is prefix
    Juan `(`de) la Cruz v. Example | is _not_ prefix
    """

    pfx = list(nlp.Defaults.prefixes)  # type: ignore
    for opened, closed in PAIRS:
        pfx.remove(f"\\{opened}")
        pfx.append(f"\\{opened}(?![\\w\\.]+\\{closed})")
    return pfx


def custom_suffix_list(nlp: spacy.language.Language):
    """Enable partner closing character, e.g. `)` or `]` to be excluded as a suffix
    if matched with an opening `(` or `[` within the range provided by `num`.

    Assuming a range of 20, this means 19 characters will be allowed:

    Let's exceed this range with 22, this results in a split of the terminal character `)`:

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

    However, if the number of characters within a closed / covered single world is 19 and below:

    ```py
    text = "smol"
    len(text)  # 4
    nlp.tokenizer.explain("A (smol)")
    # [('TOKEN', 'A'),
    # ('TOKEN', '(smol)'),
    # ('TOKEN', 'word')]
    ```

    The suffix ")" is removed per the general rule.
    """
    sfx = list(nlp.Defaults.suffixes)  # type: ignore
    for opened, closed in PAIRS:
        sfx.remove(f"\\{closed}")
        _pre = "".join([f"(?<!\\{opened}\\w{{{i}}})" for i in range(1, 20)])
        sfx.append(f"{_pre}\\{closed}")

    return sfx


def create_special_rules():
    def make_special_dotted(texts: list[str]):
        """Add a period after every text item in `texts`, to consider each a single token.
        These patterns can be used as a special rule in creating a custom tokenizer."""
        return {f"{t}.": [{"ORTH": f"{t}."}] for t in texts if not t.endswith(".")}

    x = make_special_dotted(
        "Rep Sen vs Vs v s et al etc Ll p Pp PP P.P R.P H.B S.B a.k.a".split()
    )

    a = {
        k: v
        for member in DocketNum
        if member.value.initials
        for k, v in member.value.initials.as_token.items()
    }

    b = {
        k: v
        for member in StatuteNum
        if member.value.initials
        for k, v in member.value.initials.as_token.items()
    }

    c = {
        f"{bit}.": [{"ORTH": f"{bit}."}]
        for style in (None, "lower", "upper")
        for bit in Abbv.set_abbvs(cased=style)
    }

    d = {
        f"{bit}.": [{"ORTH": f"{bit}."}]
        for style in (None, "lower", "upper")
        for bit in Prov.set_abbvs(cased=style)
    }

    return a | b | c | d | x
