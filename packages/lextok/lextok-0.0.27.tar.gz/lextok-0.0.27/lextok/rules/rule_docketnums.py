from enum import Enum
from typing import Any

from lextok.rules._pattern import Label, Rule, Style, _re


class DocketNum(Enum):
    GR = Style(let="gr")
    AM = Style(
        let="am",
        v=[
            "adm mat",
            "adm. mat",
            "adm mat.",
            "adm. mat.",
            "adm matter",
            "adm. matter",
            "admin. matter",
            "admin matter",
            "administrative matter",
        ],
    )
    AC = Style(
        let="ac",
        v=[
            "adm case",
            "adm. case",
            "admin. case",
            "admin case",
            "administrative case",
        ],
    )
    BM = Style(let="bm", v=["bar mat.", "bar matter"])


special_l: list[dict[str, Any]] = [
    {
        "TEXT": {"REGEX": "^L-\\d{4,}$", "NOT_IN": ["L-300"]}
    },  # prevent L-300 capture if not preceded by NUM
]
numbered_l: list[dict[str, Any]] = [
    {"ORTH": {"IN": ["NO", "NOS", "NO.", "NOS.", "No", "Nos", "No.", "Nos."]}},
    {"TEXT": {"REGEX": "^L-\\d{4,}$"}},
]
docket_nums = Rule(
    label=Label.DocketNum,
    patterns=[p for mem in DocketNum for p in mem.value.patterns]
    + [special_l, numbered_l],
)
