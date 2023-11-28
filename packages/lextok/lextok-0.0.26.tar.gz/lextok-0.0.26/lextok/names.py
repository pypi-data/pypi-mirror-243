import re
from itertools import permutations


def pluralize_regex_options(raw: list[str]):
    return rf"({r'|'.join(raw)})s?"


initiators = "Petitioner Respondent Plaintiff Complainant Defendant"
intervenors = [f"({i})s?-Intervenor" for i in initiators.split()]
plus = (
    "Protestant Protestee Applicant Oppositor Opponent Objector Accused Intervenor"
    " Bondsman"
)
suffix = "Appellant Appellee Intervenor"
party = " ".join([initiators, plus])

parties = pluralize_regex_options(party.split() + intervenors)
suffixes = pluralize_regex_options(suffix.split())

probable_bits = [f"{parties}-{suffixes}", f"{suffixes}-{parties}", parties, suffixes]
probable_patterns = permutations(probable_bits, r=2)
extended_bits = ["".join((p[0], r"((\s+And\s+)|-)", p[1])) for p in probable_patterns]
options = extended_bits + probable_bits

DESIGNATOR = [{"TEXT": {"REGEX": r"|".join(rf"({bit})" for bit in options)}}]


removal_designator = r"|".join(rf"((,?\s*)?{bit}$)" for bit in options)
removal_pattern = re.compile(removal_designator, re.M)


def remove_designator(text: str):
    if match := removal_pattern.search(text):
        return text.replace(match.group(), "")
    return text


def remove_suffixes(text: str):
    for suffix in ("Jr", "Jr.", "Sr", "Sr.", "Iii", "Iv"):
        text = text.removesuffix(f" {suffix}")
    return text


def prep_raw_names(text: str):
    text = text.strip(", ")
    text = remove_suffixes(text)
    text = remove_designator(text)
    return text.strip(", ")


def clean_text(text: str) -> str:
    return (
        text.replace("[*]", " ")
        .replace("[1]", " ")
        .replace("[2]", " ")
        .replace("*", " ")
        .replace("”", '"')
        .replace("“", '"')
    )


generic_name_with_middle_initial = re.compile(
    r"""
    ^
    (?P<first_name>\w+)
    \s+
    [A-Z]\.
    \s+
    (?P<last_name>\w+)
    $
    """,
    re.X,
)


def get_first_last_names(names: list[str]):
    first_names = set()
    last_names = set()
    for n in names:
        if m := generic_name_with_middle_initial.search(n):
            first_names.add(m.group("first_name"))
            last_names.add(m.group("last_name"))
    return first_names, last_names
