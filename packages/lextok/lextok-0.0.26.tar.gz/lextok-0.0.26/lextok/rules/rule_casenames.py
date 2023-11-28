import itertools
from enum import Enum
from typing import Any

from lextok.rules._pattern import VS, Label, Rule, _orth_in, _re
from lextok.rules.abbreviations import org_options, ph_options

extras = " ".join(org_options)
extras += " " + " ".join(ph_options)
extras += " . , et al. et al the Jr Jr. Sr Sr. III IV Partnership Dev't"
misc = _orth_in(extras.split()) | {"OP": "*"}
opt_acronym = _re("\\([A-Z]+\\)") | {"OP": "?"}


class CaseName(Enum):
    ent = {
        "ENT_TYPE": {
            "IN": [
                Label.ORG.name,
                Label.PERSON.name,
                Label.GovtDivision.name,
                Label.JuridicalEntity.name,
            ]
        },
        "OP": "+",
    }
    pos = {"POS": {"IN": ["PROPN", "ADP", "DET", "CCONJ"]}, "OP": "+"}
    upper = {"IS_UPPER": True, "OP": "{1,6}"}
    title = {"IS_TITLE": True, "OP": "{1,6}"}

    @staticmethod
    def _vs(first: dict[str, Any], second: dict[str, Any]) -> list[dict[str, Any]]:
        return [first, opt_acronym, misc] + [VS] + [second, opt_acronym, misc]

    @classmethod
    def permute_patterns(cls) -> list[list[dict[str, Any]]]:
        return [
            cls._vs(a, b) for a, b in itertools.permutations((m.value for m in cls), 2)
        ]


casename = Rule(label=Label.CaseName, patterns=CaseName.permute_patterns())
