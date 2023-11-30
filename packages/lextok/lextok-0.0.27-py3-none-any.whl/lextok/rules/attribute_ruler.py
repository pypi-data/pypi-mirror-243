from enum import Enum
from typing import Any, NamedTuple

from lextok.rules._pattern import CM, VS, Label, _orth_in, _re
from lextok.rules.abbreviations import Abbv


class Attr(NamedTuple):
    """Creates a repeatable pattern for spacy's `AttributeRuler` in the customized
    tokenizer: a pattern is a list of tokens where each token is represented by the
    index. The specified index in `indexes` means that the user desires to change
    the attribute of the token represented by the index with the attribute values
    set in `attrs`. See example in https://spacy.io/usage/linguistic-features#mappings-exceptions
    """

    pattern: list[dict[str, Any]]  # the list of tokens
    attrs: dict[str, Any]  # e.g. make index 0 of the `pattern`` a NUM
    indexes: list[int]  # default to the first token in the pattern
    examples: list[str] | None = None

    def create_rules(self):
        for index in self.indexes:
            yield {"patterns": [self.pattern], "attrs": self.attrs, "index": index}


class WordAttributes(Enum):
    num = Attr(
        pattern=[
            {"IS_TITLE": True},
            _orth_in(["No", "Nos", "No.", "Nos."]),
        ],
        attrs={"POS": "PROPN"},
        indexes=[0, 1],
    )

    etal1 = Attr(
        pattern=[
            {"IS_TITLE": True},
            CM,  # with comma
            {"LOWER": {"IN": ["et", "et."]}},
            {"LOWER": {"IN": ["al", "al."]}},
        ],
        attrs={"POS": "PROPN"},
        indexes=[0, 1, 2, 3],
    )

    etal2 = Attr(
        pattern=[
            {"IS_TITLE": True},  # without comma
            {"LOWER": {"IN": ["et", "et."]}},
            {"LOWER": {"IN": ["al", "al."]}},
        ],
        attrs={"POS": "PROPN"},
        indexes=[0, 1, 2],
    )

    vda_prefix = Attr(
        pattern=[_orth_in(Abbv.Vda.value.options), {"LOWER": "de"}, {"IS_ALPHA": True}],
        attrs={"POS": "PROPN", "ENT_TYPE": Label.PERSON.name},
        indexes=[0, 1, 2],
    )

    de_la = Attr(
        pattern=[{"LOWER": "de"}, {"LOWER": {"IN": ["la", "leon", "los"]}}],
        attrs={"POS": "PROPN", "ENT_TYPE": Label.PERSON.name},
        indexes=[0, 1],
    )

    dela = Attr(
        pattern=[{"ORTH": {"IN": ["de", "De", "dela", "Dela", "Delos"]}}],
        attrs={"POS": "PROPN", "ENT_TYPE": Label.PERSON.name},
        indexes=[0],
    )

    people_v = Attr(
        pattern=[{"LOWER": {"IN": ["pp", "pp.", "people", "republic", "rp"]}}, VS],
        attrs={"POS": "PROPN"},
        indexes=[0],
    )

    v_court = Attr(
        pattern=[VS, {"ORTH": {"IN": ["CA", "CFI", "Sandiganbayan"]}}],
        attrs={"POS": "PROPN"},
        indexes=[1],
    )

    dot_pre_v = Attr(
        pattern=[{"IS_ASCII": True}, {"ORTH": "."}, VS],
        attrs={"POS": "PROPN", "IS_PUNCT": False},
        indexes=[0, 1],
    )

    person_suffix_pre_v = Attr(
        pattern=[CM, {"ORTH": {"IN": ["Jr.", "Sr."]}}, VS],
        attrs={"POS": "PROPN"},
        indexes=[0, 1],
    )

    person_suffix_pre_v2 = Attr(
        pattern=[
            {"IS_TITLE": True},
            {"ORTH": {"IN": ["Jr.", "Sr.", "II", "III", "IV", "V", "VI"]}},
            VS,
        ],
        attrs={"POS": "PROPN"},
        indexes=[0, 1],
    )

    v = Attr(
        pattern=[VS],
        attrs={"TAG": "NNP", "POS": "CCONJ"},
        indexes=[0],
    )

    @classmethod
    def make_attr_rules(cls):
        for member in cls:
            for rules in member.value.create_rules():
                yield rules  # type: ignore
