from enum import Enum

from lextok.rules._pattern import Label, Rule, Style


class StatuteNum(Enum):
    RA = Style(let="ra", r="\\d{1,5}", v=["republic act", "rep. act"])
    CA = Style(let="ca", r="\\d{1,3}", v=["commonwealth act", "com. act"])
    BP = Style(let="bp", r="\\d{1,3}(-?(A|B))?", v=["batas pambansa"], pre=["Blg."])
    EO = Style(let="eo", r="\\d{1,4}(-?(A|B|C))?", v=["executive order", "exec. order"])
    PD = Style(
        let="pd",
        r="\\d{1,4}(-?(A|B))?",
        v=["presidential decree", "pres. decree", "pres. dec."],
    )
    ACT = Style(r="\\d{1,4}", v=["act"])


statute_nums = Rule(
    label=Label.StatuteNum,
    patterns=[p for mem in StatuteNum for p in mem.value.patterns],
)
