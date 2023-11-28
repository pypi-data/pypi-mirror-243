from typing import Any

from lextok.rules._pattern import (
    CM,
    OF,
    Label,
    Rule,
    _orth_in,
    _re,
    create_regex_options,
)
from lextok.rules.abbreviations import Abbv

months = [
    month
    for defined_month in (
        Abbv.January,
        Abbv.February,
        Abbv.March,
        Abbv.April,
        Abbv.May,
        Abbv.June,
        Abbv.July,
        Abbv.August,
        Abbv.Sept1,
        Abbv.Sept2,
        Abbv.October,
        Abbv.November,
        Abbv.December,
    )
    for month in defined_month.value.options
]

days = _orth_in([f"{str(i)}" for i in range(1, 32)] + [f"0{i}" for i in range(1, 10)])

ranged_years = create_regex_options(["(19\\d{2})", "(20\\d{2})"])

date_us: list[list[dict[str, Any]]] = [
    [CM | {"OP": "?"}, {"ORTH": month_name}, days, CM | {"OP": "?"}, _re(ranged_years)]
    for month_name in months  # , Feb. 01, 2023
]

date_uk: list[list[dict[str, Any]]] = [
    [CM | {"OP": "?"}, days, {"ORTH": month_name}, CM | {"OP": "?"}, _re(ranged_years)]
    for month_name in months  # 01 Feb 2023
]


covered_parent_year: list[dict[str, Any]] = [
    _re("\\(" + ranged_years + "\\)"),  # (2023)
]


covered_bracket_year: list[dict[str, Any]] = [
    _re("\\[" + ranged_years + "\\]"),  # [2023]
]

series_year: list[dict[str, Any]] = [
    CM | {"OP": "?"},
    {"LOWER": {"IN": ["s.", "series"]}},  # , s. of 2023
    OF | {"OP": "?"},
    _re(ranged_years),
]

date_special = [covered_parent_year, covered_bracket_year, series_year]

date_as_entity = Rule(
    label=Label.DATE,
    patterns=date_us + date_uk + date_special,
)
