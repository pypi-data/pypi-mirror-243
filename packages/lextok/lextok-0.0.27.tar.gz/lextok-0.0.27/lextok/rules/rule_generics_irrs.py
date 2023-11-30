from typing import Any

from lextok.rules._pattern import OPT_NUMS, Label, Rule

up: dict[str, Any] = {"IS_UPPER": True, "OP": "+"}
tit: dict[str, Any] = {"IS_TITLE": True, "OP": "+"}
opt_tit: dict[str, Any] = {"IS_TITLE": True, "OP": "*"}
opt_cover: dict[str, Any] = {"TEXT": {"REGEX": "\\(.*\\)"}, "OP": "?"}
cov_num: list[dict[str, Any]] = [opt_cover, Label.GenericNum.node]
plus_date: list[dict[str, Any]] = [OPT_NUMS, Label.DATE.node]

doc_variants: list[list[dict[str, Any]]] = [
    [up, tit] + cov_num + plus_date,
    [up] + cov_num + plus_date,
    [tit] + cov_num + plus_date,
    [up, tit] + cov_num,
    [up] + cov_num,
    [tit] + cov_num,
    [up, tit, Label.GenericNum.node],
    [up, Label.GenericNum.node],
    [tit, Label.GenericNum.node],
    [Label.ORG.node, Label.GenericNum.node],
]
generic_documents = Rule(label=Label.Candidate, patterns=doc_variants)
"""Connect a generic serial number with a date, e.g. `Doc No. 414, Jan. 15, 2000`"""


irr_variants: list[list[dict[str, Any]]] = [
    [
        {"LOWER": "rules", "IS_TITLE": True},
        {"LOWER": "and", "IS_LOWER": True},
        {"LOWER": "regulations", "IS_TITLE": True},
        {"LOWER": "implementing", "IS_TITLE": True},
        {"IS_TITLE": True, "OP": "*"},
    ],
    [
        {"LOWER": "implementing", "IS_TITLE": True},
        {"LOWER": "rules", "IS_TITLE": True},
        {"LOWER": "and", "IS_LOWER": True},
        {"LOWER": "regulations", "IS_TITLE": True},
        {"ORTH": {"IN": ["of", "the"]}, "OP": "*"},
        {"IS_TITLE": True, "OP": "*"},
    ],
    [
        {"LOWER": {"IN": ["old", "new", "pre"]}, "IS_LOWER": True, "OP": "?"},
        {"ORTH": "-", "OP": "?"},
        {"SHAPE": "dddd", "OP": "?"},  # 1997, 1964, 2004
        {"IS_UPPER": True, "OP": "*"},  # NLRC, COMELEC, DARAB, Revised
        {"IS_TITLE": True, "OP": "*"},  # Revised
        {"LOWER": {"IN": ["rule", "rules"]}, "IS_TITLE": True},
        {"LOWER": {"IN": ["on", "of"]}},
        {"IS_TITLE": True, "OP": "*"},
    ],
    [
        {"SHAPE": "dddd", "OP": "?"},  # 1997, 1964, 2004
        {"IS_UPPER": True, "OP": "*"},  # NLRC
        {"IS_TITLE": True, "OP": "*"},  # Revised
        {"LOWER": "revised", "OP": "?"},
        {
            "LOWER": {"IN": ["omnibus", "uniform", "implementing", "rules", "interim"]},
            "IS_TITLE": True,
            "OP": "+",
        },
    ],
]
opt_connect: dict[str, Any] = {"ORTH": {"IN": ["of", "the", ","]}, "OP": "*"}

generic_irrs = Rule(label=Label.Candidate, patterns=irr_variants)


prov_irr = Rule(
    label=Label.CandidateProvision,
    patterns=[
        [{"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}, opt_connect] + i
        for i in irr_variants
    ]
    + [
        [{"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}, opt_connect] + d
        for d in doc_variants
    ],
)
