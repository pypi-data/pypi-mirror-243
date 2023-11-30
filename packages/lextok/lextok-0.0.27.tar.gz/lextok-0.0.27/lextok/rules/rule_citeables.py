from enum import Enum
from typing import Any

from lextok.rules._pattern import CM, OPT_NUMS, Label, Rule, _multi, _re

dig = {"IS_DIGIT": True}
pages = {"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"}
covered = {"TEXT": {"REGEX": "^\\(\\d+\\)$"}, "OP": "?"}
publisher_short = {"ORTH": {"IN": ["SCRA", "Phil", "Phil.", "OG", "O.G."]}}
publisher_words_phil = [
    {"ORTH": {"IN": ["Phil", "Phil."]}},
    {"ORTH": {"IN": ["Rep", "Rep.", "Reports"]}},
]
publisher_words_og = [
    {"ORTH": {"IN": ["Off", "Off."]}},
    {"ORTH": {"IN": ["Gaz", "Gazette"]}},
]

generic_start: list[dict[str, Any]] = [dig, publisher_short, pages]
generic_start_phil_words: list[dict[str, Any]] = [dig] + publisher_words_phil + [pages]
generic_start_og_words: list[dict[str, Any]] = [dig] + publisher_words_og + [pages]
special_volumes: list[dict[str, Any]] = [
    {"ORTH": {"IN": ["258-A", "290-A", "8-A"]}},  # Dashed letter vs. digit
    publisher_short,
    dig,
]
connected_comma_pages: list[dict[str, Any]] = [
    dig,
    publisher_short,
    {"TEXT": {"REGEX": "\\d+[,-]\\d+"}},  # 21 Phil 124,125
]
og_legacy: list[dict[str, Any]] = [
    dig,
    covered,
    {"ORTH": {"IN": ["OG", "O.G."]}},
    covered,
]


reporter_nums = Rule(
    label=Label.ReporterNum,
    patterns=[
        generic_start + [dig],
        generic_start + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
        generic_start_phil_words + [dig],
        generic_start_phil_words + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
        generic_start_og_words + [dig],
        generic_start_og_words + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
        connected_comma_pages,
        special_volumes,
        og_legacy + [dig],
        og_legacy + [{"LIKE_NUM": True}],  # e.g. fourth, fifth
    ],
)


stat = {
    "ENT_TYPE": {
        "IN": [
            Label.StatuteNamed.name,
            Label.StatuteNum.name,
            Label.DocketNum.name,
        ]
    }
}

opt_comma_plus = {"ORTH": {"IN": ["of", "the", ","]}, "OP": "*"}

linker = {"ORTH": {"IN": ["or", "and", ",", "&"]}, "OP": "+"}

multi_linked_statute_pattern = _multi([linker, stat], 10)  # type: ignore
for linked_list in multi_linked_statute_pattern:
    linked_list.insert(0, stat)
as_amended: list[dict[str, Any]] = [
    {"ORTH": ",", "IS_PUNCT": True, "OP": "?"},
    {"LOWER": "as", "OP": "?"},
    {"LOWER": "amended"},
    {"LOWER": "by", "OP": "?"},
]

linked_statutes = Rule(
    label=Label.StatutoryLink,
    patterns=multi_linked_statute_pattern + [[stat] + as_amended + [stat]],
)
"""Connect statutory numbers together: `RA 141, RA 4124, RA 5325`"""

statutory_provisions = Rule(
    label=Label.StatutoryProvision,
    patterns=[
        [{"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}, opt_comma_plus, stat],
        [stat, opt_comma_plus, {"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}],
    ],
)
"""Connect statutes with provisions: `Art. 2, Civil Code`"""


decision_citations = Rule(
    label=Label.DecisionCitation,
    patterns=[
        [
            Label.DocketNum.node,
            OPT_NUMS,
            Label.DATE.node,
            CM | {"OP": "?"},
            Label.ReporterNum.node,
        ],
        [
            Label.DocketNum.node,
            OPT_NUMS,
            Label.DATE.node,
        ],
        [
            Label.ReporterNum.node,
            OPT_NUMS,
            CM | {"OP": "?"},
            Label.DATE.node,
        ],
    ],
)
"""Connect decision names, docket citations, date, and/or reporter numbers: `X v. Y, GR No. 3425, Jan. 1, 2000, 14 SCRA 14`"""
