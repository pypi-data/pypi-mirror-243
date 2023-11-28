# lextok

![Github CI](https://github.com/justmars/lextok/actions/workflows/main.yml/badge.svg)

Rule-based tokenizer and pattern matching for basic Philippine entities using spacy.

> [!IMPORTANT]
> Should be used in tandem with [doclex](https://github.com/justmars/doclex)

## Quickstart

```sh
poetry env use 3.11.6 # 3.12 not yet supported
poetry install
poetry shell
python -m spacy download en_core_web_sm # base model
```

## Rationale

### Before

```py
import spacy

nlp = spacy.load("en_core_web_sm")  # no modifications to the model
doc1 = nlp("Sec. 36(b)(21)")
for token in doc1:
    print(f"{token.text=} {token.pos_=} {token.ent_type_=}, {token.i=}")
"""
token.text='Sec' token.pos_='PROPN' token.ent_type_='ORG' token.i=0
token.text='.' token.pos_='PUNCT' token.ent_type_='' token.i=1
token.text='36(b)(21' token.pos_='NUM' token.ent_type_='CARDINAL' token.i=2
token.text=')' token.pos_='PUNCT' token.ent_type_='' token.i=3
"""
```

### After

```py
from lextok import lextok

lex = lextok()  # inclusion of custom tokenizer, attribute and entity ruler
doc2 = lex("Sec. 36(b)(21)")
for token in doc2:
    print(f"{token.text=} {token.pos_=} {token.ent_type_=} {token.i=}")
"""
token.text='Sec.' token.pos_='NOUN' token.ent_type_='ProvisionNum' token.i=0
token.text='36(b)(21)' token.pos_='NUM' token.ent_type_='ProvisionNum' token.i=1
"""
```

Token entities can be merged:

```py
from lextok import lextok

lex = lextok(finalize_entities=True)
doc2 = lex("Sec. 36(b)(21)")
for token in doc2:
    print(f"{token.text=} {token.pos_=} {token.ent_type_=} {token.i=}")
"""
token.text='Sec. 36(b)(21)' token.pos_='NUM' token.ent_type_='ProvisionNum' token.i=0
"""
```

## Pattern creation

A pattern consists of a list of tokens, e.g. space space between the word, a dot, and the number?

```py
[
    {"ORTH": {"IN": ["Tit", "Bk", "Ch", "Sub-Chap", "Art", "Sec", "Par", "Sub-Par"]}},
    {"ORTH": "."},  # with dot
    {"POS": "NUM"},
]
```

This is another pattern where the dot is connected to the word:

```py
[
    {
        "ORTH": {
            "IN": [
                "Tit.",
                "Bk.",
                "Ch.",
                "Sub-Chap.",
                "Art.",
                "Sec.",
                "Par.",
                "Sub-Par.",
            ]
        }
    },
    {"POS": "NUM"},
]  # no separate dot
```

There are many variations. It becomes possible to generate a list of patterns algorithmically and save them to a `*.jsonl` file, e.g.:

```py
from lextok.entity_rules_citeable import statutory_provisions

print(statutory_provisions.patterns)  # view patterns
statutory_provisions.create_file()  # located in /lextok/rules/ if path not specified
```

## Rules and Labels

Each `Rule` may consist of many _patterns_, and this collection of patterns can be associated with a `Label`.

In spacy parlance, the label represents the `ENT_TYPE` but for this library's purpose, it's also adopted for non-entities to cater to _SpanRuler_ patterns.

To distinguish labels strictly for entities from labels for non-entities, a collection of labels is defined in `SPAN_RULER_LABELS`. If not included in this list of labels, then the implication is that the Rule's patterns ought to be governed by the _EntityRuler_; otherwise, the _SpanRuler_.

Considering the number of `Rules` declared (or to be declared), instead of importing each instance individually, these can be extracted dynamically with `Rule.extract_from_files()`.

### Existing data structures

```py
from lextok import Label, ENTITY_RULES, SPAN_RULES

for label in Label:
    print(label.name)  # pattern labels
for e in ENTITY_RULES:
    print(e)
for s in SPAN_RULES:
    print(s)
```

### Add more entity rules

Create a list of `Rule` objects, e.g.:

```py
from lextok import lextok, Rule, ENTITY_RULES, Label

added_rules = [
    Rule(
        id="ministry-labor",
        label=Label.GovtDivision,
        patterns=[
            [
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "ministry"},
                {"LOWER": "of"},
                {"LOWER": "labor"},
            ]
        ],
    ),
    Rule(
        id="intermediate-scrutiny",
        label=Label.Doctrine,
        patterns=[
            [
                {"LOWER": "test", "OP": "?"},
                {"LOWER": "of", "OP": "?"},
                {"LOWER": "intermediate"},
                {"LOWER": "scrutiny"},
                {"LEMMA": {"IN": ["test", "approach"]}, "OP": "?"},
            ]
        ],
    ),
]

# Include new rules in lextok language
nlp = lextok(finalize_entities=True, entity_rules=ENTITY_RULES + added_rules)

# Test detection
doc = nlp(
    "Lorem ipsum, sample text. The Ministry of Labor is a govt division. Hello world. The test of intermediate scrutiny is a constitutional law concept."
)
doc.ents  # (The Ministry of Labor, test of intermediate scrutiny)
```
