from lextok.rules._pattern import Label, Rule, _orth_in

prefix_tits = _orth_in(["Atty.", "Hon.", "Engr.", "Dr.", "Dra."])
prefix_titled_person = Rule(
    label=Label.PERSON,
    patterns=[
        [prefix_tits, {"IS_TITLE": True, "OP": "+"}],
        [prefix_tits, {"ENT_TYPE": Label.PERSON.name}],
    ],
)
