from typing import Any

from lextok.rules._pattern import OF, THE, Label, Rule
from lextok.rules.abbreviations import org_options

inc_suffixes = list(set(o.lower() for o in org_options)) and ["gmbh"]
inc_options: list[dict[str, Any]] = [
    {"ORTH": {"IN": [",", "and", "&"]}, "OP": "*"},
    {"LOWER": {"IN": inc_suffixes}},
    {"LOWER": {"IN": inc_suffixes + [","]}, "OP": "?"},
]
juridical_org = Rule(
    label=Label.JuridicalEntity,
    patterns=[
        [
            {
                "LOWER": {
                    "IN": (
                        "rep rep. republic people pp p.p. pp. govt govt. government"
                        " gov't".split()
                    )
                }
            },
            OF,
            THE,
            {"LOWER": {"IN": "phil phils phil. phils. philippines".split()}},
        ],
        [{"IS_UPPER": True, "OP": "+"}] + inc_options,
        [{"IS_TITLE": True, "OP": "+"}] + inc_options,
        [{"ORTH": "Province"}, OF, {"IS_TITLE": True, "OP": "+"}],
        [{"ORTH": "City"}, OF, {"IS_TITLE": True, "OP": "+"}],
        [{"ORTH": "Municipality"}, OF, {"IS_TITLE": True, "OP": "+"}],
        [{"ORTH": "Estate"}, OF, {"IS_TITLE": True, "OP": "+"}],
    ],
)
