from collections.abc import Iterator
from enum import Enum
from typing import Any, NamedTuple

from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from lextok.rules._pattern import PROV_DIGITS, _orth_in, _re


def check_titlecased_word(v: str) -> str:
    assert all(bit.istitle for bit in v.split("-")), f"{v} is not titlecased."
    return v


TitledString = Annotated[str, AfterValidator(check_titlecased_word)]


class Def(NamedTuple):
    """A (possible) definition of a commonly used abbreviation;
    each value must be a `TitledString` so that it can be
    adjusted for lowercase / uppercase variants."""

    title: TitledString
    abbv: TitledString | None = None

    @staticmethod
    def get_cased_value(v: str, cased: str | None = None) -> str:
        if cased:
            if cased == "lower":
                return v.lower()
            elif cased == "upper":
                return v.upper()
        return v

    @property
    def dotted_abbv(self) -> list[str]:
        bits = []
        if self.abbv:
            for style in (None, "lower", "upper"):
                bits.append(self.get_cased_value(self.abbv, cased=style))
                bits.append(self.get_cased_value(self.abbv + ".", cased=style))
        return bits

    @property
    def options(self) -> list[str]:
        bits = []
        for style in (None, "lower", "upper"):
            bits.append(self.get_cased_value(self.title, cased=style))
        return bits + self.dotted_abbv


class Abbv(Enum):
    """Some common abbreviations used in Philippine legal text."""

    Adm = Def(title="Administrative", abbv="Adm")
    Admin = Def(title="Administrative", abbv="Admin")
    Pres = Def(title="Presidential", abbv="Pres")
    Dec = Def(title="Decree", abbv="Dec")
    Executive = Def(title="Executive", abbv="Exec")
    Blg = Def(title="Bilang", abbv="Blg")
    Number = Def(title="Number", abbv="No")
    Numbers = Def(title="Numbers", abbv="Nos")
    Const = Def(title="Constitution", abbv="Const")
    Company = Def(title="Company", abbv="Co")
    Corporation = Def(title="Corporation", abbv="Corp")
    Incorporated = Def(title="Incorporated", abbv="Inc")
    Phil1 = Def(title="Philippines", abbv="Phil")
    Phil2 = Def(title="Philippines", abbv="Phils")
    Limited = Def(title="Limited", abbv="Ltd")
    Association = Def(title="Association", abbv="Assoc")
    Assistant = Def(title="Assistant", abbv="Ass")
    Department = Def(title="Department", abbv="Dept")
    Nat1 = Def(title="National", abbv="Nat")
    Nat2 = Def(title="National", abbv="Natl")
    St = Def(title="Street", abbv="St")
    Road = Def(title="Road", abbv="Rd")
    Ave = Def(title="Avenue", abbv="Ave")
    Blk = Def(title="Block", abbv="Blk")
    Brgy = Def(title="Barangay", abbv="Brgy")
    Building = Def(title="Building", abbv="Bldg")
    Purok = Def(title="Purok", abbv="Prk")
    Subdivision = Def(title="Subdivision", abbv="Subd")
    Highway = Def(title="Highway", abbv="Hwy")
    Municipality = Def(title="Municipality", abbv="Mun")
    City = Def(title="City", abbv="Cty")
    Province = Def(title="Province", abbv="Prov")
    Governor = Def(title="Governor", abbv="Gov")
    Congressman = Def(title="Congressman", abbv="Cong")
    General = Def(title="General", abbv="Gen")
    Lieutenant = Def(title="Lieutenant", abbv="Lt")
    Sct = Def(title="Scout", abbv="Sct")
    Sta = Def(title="Santa", abbv="Sta")
    Sto = Def(title="Santo", abbv="Sto")
    Vda = Def(title="Viuda", abbv="Vda")
    Jr = Def(title="Junior", abbv="Jr")
    Sr = Def(title="Senior", abbv="Sr")
    Fr = Def(title="Father", abbv="Fr")
    Bro = Def(title="Brother", abbv="Bro")
    Dr = Def(title="Doctor", abbv="Dr")
    Dra = Def(title="Doctora", abbv="Dra")
    Maria = Def(title="Maria", abbv="Ma")
    Hon = Def(title="Honorable", abbv="Hon")
    Atty = Def(title="Attorney", abbv="Atty")
    Engr = Def(title="Engineer", abbv="Engr")
    Justice = Def(title="Justice", abbv="J")
    January = Def(title="January", abbv="Jan")
    February = Def(title="February", abbv="Feb")
    March = Def(title="March", abbv="Mar")
    April = Def(title="April", abbv="Apr")
    May = Def(title="May")
    June = Def(title="June", abbv="Jun")
    July = Def(title="July", abbv="Jul")
    August = Def(title="August", abbv="Aug")
    Sept1 = Def(title="September", abbv="Sept")
    Sept2 = Def(title="September", abbv="Sep")
    October = Def(title="October", abbv="Oct")
    November = Def(title="November", abbv="Nov")
    December = Def(title="December", abbv="Dec")

    @classmethod
    def set_abbvs(cls, cased: str | None = None) -> Iterator[str]:
        for member in cls:
            if v := member.value.abbv:
                yield Def.get_cased_value(v, cased)

    @classmethod
    def set_fulls(cls, cased: str | None = None) -> Iterator[str]:
        for member in cls:
            yield Def.get_cased_value(member.value.title, cased)


class Prov(Enum):
    """A ProvisionNum of a statute may be abbreviated and the same may have different variations:
    e.g. titlecase, lowercase, and uppercase."""

    Title = Def(title="Title", abbv="Tit")
    SubT0 = Def(title="Subtitle")
    SubT1 = Def(title="SubTitle")
    SubT2 = Def(title="Sub-Title")
    Book = Def(title="Book", abbv="Bk")
    Chapter = Def(title="Chapter", abbv="Ch")
    SubChap0 = Def(title="Subchapter")
    SubChap1 = Def(title="SubChapter")
    SubChap2 = Def(title="Sub-Chapter", abbv="Sub-Chap")
    Article = Def(title="Article", abbv="Art")
    SubArt0 = Def(title="Subarticle")
    SubArt1 = Def(title="SubArticle")
    SubArt2 = Def(title="Sub-Article", abbv="Sub-Art")
    Section = Def(title="Section", abbv="Sec")
    SubSec0 = Def(title="Subsection")
    SubSec1 = Def(title="SubSection")
    SubSec2 = Def(title="Sub-Section", abbv="Sub-Sec")
    Par = Def(title="Paragraph", abbv="Par")
    SubPar0 = Def(title="Subparagraph")
    SubPar1 = Def(title="SubParagraph")
    SubPar2 = Def(title="Sub-Paragraph", abbv="Sub-Par")
    ProvRule = Def(title="Rule")
    Canon = Def(title="Canon")

    @classmethod
    def make_attr_rules(cls) -> Iterator[dict[str, Any]]:
        """Each member can contain explicit rules so that "digit patterns"
        are paired with the "adjective patterns":

        first node (adjective) | second node (digit)
        :-- | --:
        The member option for Sec., Section, etc. | a "digit" pattern e.g. 1, 1(a)

        The list of patterns can then be applied as part of an attribute ruler
        https://spacy.io/usage/linguistic-features#mappings-exceptions so that
        the token in the second node, i.e. the digit, can be set with the attributes defined in
        `attributes_to_set`.
        """
        for member in cls:
            p = [[{"ORTH": o}, p] for p in PROV_DIGITS for o in member.value.options]
            yield {
                "index": 0,
                "patterns": p,
                "attrs": {"POS": "NOUN"},
            }
            yield {
                "index": 1,
                "patterns": p,
                "attrs": {"POS": "NUM", "LIKE_NUM": True, "IS_DIGIT": True},
            }

    @classmethod
    def set_abbvs(cls, cased: str | None = None):
        for member in cls:
            if v := member.value.abbv:
                yield Def.get_cased_value(v, cased)

    @classmethod
    def set_fulls(cls, cased: str | None = None):
        for member in cls:
            yield Def.get_cased_value(member.value.title, cased)


org_options = set(
    op
    for s in (Abbv.Company, Abbv.Corporation, Abbv.Limited, Abbv.Incorporated)
    for op in s.value.options
)
ph_options = set(op for s in (Abbv.Phil1, Abbv.Phil2) for op in s.value.options)
