from enum import Enum

from lextok.rules._pattern import COURT, Label, Rule, name_court, titled_words


class CourtName(Enum):
    SC = [{"LOWER": "supreme", "IS_TITLE": True}, COURT]
    RTC = titled_words("regional trial court")
    CA = name_court("appeals")
    CFI = name_court("first instance")
    MeTC = titled_words("metropolitan trial court")
    MCTC = titled_words("municipal circuit court")
    MTC = titled_words("municipal trial court")
    MTCC = (
        titled_words("municipal trial court")
        + [{"LOWER": "in"}]
        + titled_words("the cities")
    )


court_names = Rule(label=Label.CourtName, patterns=[mem.value for mem in CourtName])  # type: ignore
